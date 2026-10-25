# Uso: python3 sons.py   (precisa de numpy e scipy; rode depois do _sistema/render-video.js)
# Sintetiza a trilha e os efeitos sonoros, sincronizados com a linha do tempo de animacao.html,
# grava sons.wav e junta com o video.mp4 (só imagem) em vinheta-adullam-com-som.mp4, sem recodificar o vídeo.
import os, subprocess
import numpy as np
from scipy import signal
from scipy.io import wavfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 14.0
N = int(SR * DUR)
rng = np.random.default_rng(11)

# Mesma linha do tempo do objeto T em animacao.html
T = dict(pouso0=0.3, hop=0.6, bola=2.1, abre=4.15, abreDur=1.15, letras=5.45, letraGap=0.1, tag=6.3,
         desliza=6.7, traco=6.9, preenche=7.5, revela=7.6, fecha=8.0, fechaDur=1.15, uivo=9.7, volta=12.05, sai=12.7)

seco = np.zeros((2, N))
envio = np.zeros((2, N))   # vai para o reverb


def tt(d):
    return np.arange(int(d * SR)) / SR


def ruido(d):
    return rng.standard_normal(int(d * SR))


def filtro(x, tipo, f, ordem=2):
    sos = signal.butter(ordem, f, btype=tipo, fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def fase(f):
    return 2 * np.pi * np.cumsum(f) / SR


def ataque(x, a=0.002):
    n = min(len(x), max(1, int(a * SR)))
    x = x.copy(); x[:n] *= np.linspace(0, 1, n)
    return x


def por(x, t, ganho=1.0, pan=0.0, rev=0.15):
    """Coloca o som x no tempo t. pan de -1 (esq.) a 1 (dir.), pode ser um array do tamanho de x."""
    i = int(t * SR)
    if i >= N:
        return
    x = x[:N - i] * ganho
    p = pan[:len(x)] if np.ndim(pan) else pan
    esq, dir_ = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
    seco[0, i:i + len(x)] += x * esq; seco[1, i:i + len(x)] += x * dir_
    envio[0, i:i + len(x)] += x * esq * rev; envio[1, i:i + len(x)] += x * dir_ * rev


# ---------- Instrumentos ----------
def pop(f, d=0.22):
    """Bolha: seno com a altura caindo rápido, mais um clique."""
    t = tt(d)
    s = np.sin(fase(f * (1 + 1.4 * np.exp(-t / 0.012)))) * np.exp(-t / 0.055)
    c = filtro(ruido(d), 'highpass', 3000) * np.exp(-t / 0.002) * 0.25
    return ataque(s + c)


def tok(f=1150, d=0.12):
    """Batida seca de bolinha."""
    t = tt(d)
    s = np.sin(fase(f * (1 + 0.35 * np.exp(-t / 0.004)))) * np.exp(-t / 0.028)
    c = filtro(ruido(d), 'bandpass', [2000, 7000]) * np.exp(-t / 0.006) * 0.4
    return ataque(s + c, 0.0008)


def pluck(f, d=0.9):
    """Nota de marimba/pluck."""
    t = tt(d)
    s = (np.sin(fase(np.full_like(t, f))) * np.exp(-t / 0.32)
         + 0.35 * np.sin(fase(np.full_like(t, 2 * f))) * np.exp(-t / 0.12)
         + 0.12 * np.sin(fase(np.full_like(t, 4.02 * f))) * np.exp(-t / 0.05))
    return ataque(s, 0.003)


def baque(f=55, d=0.9, queda=0.35):
    """Grave de impacto: seno com a altura caindo, mais ruído grave."""
    t = tt(d)
    s = np.sin(fase(f * (1 + 1.2 * np.exp(-t / 0.03)))) * np.exp(-t / queda)
    r = filtro(ruido(d), 'lowpass', 400) * np.exp(-t / 0.05) * 0.5
    # camada média para o impacto aparecer também em alto-falante de celular
    m = np.sin(fase(3 * f * (1 + 1.2 * np.exp(-t / 0.02)))) * np.exp(-t / 0.08) * 0.35
    return ataque(s + r + m, 0.002)


def sopro(d, f0, f1, forma, largura=0.5):
    """Whoosh: ruído com uma faixa de frequência que passa de f0 a f1; forma é a curva de volume (0..1)."""
    x = ruido(d + 0.1)
    f, quadros, Z = signal.stft(x, fs=SR, nperseg=1024)
    u = np.clip(quadros / d, 0, 1)
    centro = np.exp(np.log(f0) + (np.log(f1) - np.log(f0)) * u)
    lf = np.log(np.maximum(f, 1))[:, None]
    Z *= np.exp(-((lf - np.log(centro)[None, :]) / largura) ** 2)
    _, y = signal.istft(Z, fs=SR, nperseg=1024)
    y = y[:int(d * SR)]
    y /= np.max(np.abs(y)) + 1e-9
    return y * forma(np.linspace(0, 1, len(y)))


def zip_(d, f0, f1, curva=lambda u: u):
    """Tom subindo (traço sendo desenhado)."""
    u = np.linspace(0, 1, int(d * SR))
    f = f0 + (f1 - f0) * curva(u)
    ph = fase(f)
    s = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph)
    return s * np.sin(np.pi * u) ** 0.6


def uivo(d=1.8):
    """Uivo sintetizado: síntese aditiva com formantes de 'uuu', vibrato e respiração."""
    t = tt(d)
    sm = lambda x: x * x * (3 - 2 * x)
    f0 = np.where(t < 0.35, 300 + 260 * sm(np.clip(t / 0.35, 0, 1)),
         np.where(t < 1.25, 560 + 55 * (t - 0.35) / 0.9,
                  615 - 190 * sm(np.clip((t - 1.25) / (d - 1.25), 0, 1))))
    prof = 0.013 * np.clip((t - 0.35) / 0.4, 0, 1)
    f0 = f0 * (1 + prof * np.sin(2 * np.pi * 5.2 * t)) * (1 + 0.004 * filtro(ruido(d), 'lowpass', 8))
    ph = fase(f0)
    g = lambda hf, c, b: np.exp(-((hf - c) / b) ** 2)
    s = np.zeros_like(t)
    for h in range(1, 14):
        hf = h * f0
        w = g(hf, 420, 200) + 0.55 * g(hf, 900, 260) + 0.12 * g(hf, 2700, 500) + 0.02
        s += w * np.sin(h * ph) / h ** 0.3
    vol = np.clip(t / 0.14, 0, 1) * np.clip((d - t) / 0.55, 0, 1) ** 1.5
    respira = filtro(ruido(d), 'bandpass', [500, 2600]) * 0.05
    y = (s / np.max(np.abs(s)) + respira) * vol
    return y


def pad(freqs, d, corte=1100):
    """Acorde de fundo: serras desafinadas, filtradas, em estéreo."""
    t = tt(d)
    e = np.zeros((2, len(t)))
    for f in freqs:
        for lado, desaf in ((0, -0.004), (1, 0.004)):
            e[lado] += signal.sawtooth(fase(np.full_like(t, f * (1 + desaf))) + rng.uniform(0, 6.28))
    e = np.array([filtro(c, 'lowpass', corte, 2) for c in e])
    return e / len(freqs)


# ---------- Trilha de fundo: Lá menor → Fá → Lá menor ----------
A_m = [110.0, 164.81, 196.0, 246.94, 261.63]
F_maj = [87.31, 130.81, 174.61, 220.0, 329.63]
trilha = np.zeros((2, N))
for acorde, t0, t1 in ((A_m, 0.0, 5.45), (F_maj, 5.15, 9.35), (A_m, 9.05, DUR)):
    p = pad(acorde, t1 - t0 + 0.01, 1300 if t0 > 9 else 1000)
    n0 = int(t0 * SR); n = min(p.shape[1], N - n0)
    cf = np.ones(n); m = int(0.3 * SR)
    if t0 > 0: cf[:m] = np.linspace(0, 1, m)
    if t1 < DUR: cf[-m:] = np.linspace(1, 0, m)
    trilha[:, n0:n0 + n] += p[:, :n] * cf
tg = np.arange(N) / SR
vol = np.clip(tg / 1.2, 0, 1) * np.clip((DUR - tg) / 1.0, 0, 1)
vol *= 1 - 0.45 * np.exp(-((tg - 11.2) / 0.9) ** 2)          # abre espaço para o uivo
trilha *= vol * 0.10
seco += trilha; envio += trilha * 0.3

# ---------- Cena 1: cápsula quicando (#011) ----------
notas = [440.0, 523.25, 659.25, 880.0]
for i, f in enumerate(notas):
    tp = T['pouso0'] + T['hop'] * i
    por(pop(f), tp - 0.005, 0.55, pan=-0.25 + 0.17 * i)
    por(baque(90, 0.25, 0.07), tp, 0.35, rev=0.05)

# #123: a mesma física da animação (gravidade, 56% de rebote) dá o tempo de cada quique
G, REST, VMIN = 1900 * 2, 0.56, 35 * 2
t, v = T['bola'] + 0.06, np.sqrt(2 * G * 190 * 2)
v0 = v
while v > VMIN:
    t += 2 * v / G
    por(tok(1150 + 200 * (1 - v / v0)), t, 0.5 * (v / v0) ** 0.8, pan=0.0)
    v *= REST

# círculo abrindo (#017): whoosh que acompanha a velocidade da curva
d = T['abreDur']
por(sopro(d, 250, 2600, lambda u: np.sin(np.pi * u) ** 1.5), T['abre'], 0.5, rev=0.3)
por(baque(48, 1.2, 0.5), T['abre'] + d - 0.05, 0.16, rev=0.2)

# letras caindo (#011): pentatônica de Lá subindo
penta = [440.0, 523.25, 587.33, 659.25, 783.99, 880.0, 1046.5]
for i, f in enumerate(penta):
    tl = T['letras'] + T['letraGap'] * i + 0.3
    por(pluck(f), tl, 0.2, pan=-0.5 + i / 6, rev=0.35)
    por(tok(700, 0.06), tl, 0.12)

# tagline: brilho
for j, f in enumerate([1760.0, 2093.0, 2637.0, 3520.0]):
    por(pluck(f, 0.5), T['tag'] + 0.05 * j, 0.07, pan=0.3, rev=0.6)

# distintivo (#004): deslize, traço subindo, preenchimento e revelação
por(sopro(0.5, 400, 1500, lambda u: np.sin(np.pi * u)), T['desliza'], 0.18, pan=0.3)
por(zip_(0.6, 500, 1500, lambda u: np.where(u < .5, 4 * u ** 3, 1 - (-2 * u + 2) ** 3 / 2)), T['traco'], 0.07, pan=-0.6, rev=0.3)
por(pop(260, 0.3), T['preenche'], 0.45, pan=-0.6)
por(sopro(0.3, 600, 3000, lambda u: np.sin(np.pi * u)), T['revela'], 0.2, pan=-0.6)

# fundo fechando no logo: whoosh ao contrário, impacto grave e brilho no balanço (#010)
d = T['fechaDur']
por(sopro(d, 4000, 300, lambda u: u ** 2.2), T['fecha'], 0.5, rev=0.25)
t_imp = T['fecha'] + d
por(baque(42, 1.6, 0.7), t_imp, 0.26, rev=0.35)
for j, f in enumerate([880.0, 1318.5, 1760.0]):
    por(pluck(f, 1.2), t_imp + 0.02 + 0.06 * j, 0.12, rev=0.6)

# ---------- Uivo (#121 + #125) ----------
por(sopro(0.75, 300, 1400, lambda u: u ** 1.5 * (1 - u) ** 0.3), T['uivo'], 0.12, pan=-0.6)   # respiração antes
u_ = uivo(1.8)
por(u_, T['uivo'] + 0.82, 0.55, pan=-0.45, rev=0.55)
tb = T['uivo'] + 1.1
por(baque(60, 0.4, 0.12), tb + 0.2, 0.55, pan=-0.45)        # lub
por(baque(70, 0.4, 0.10), tb + 0.44, 0.32, pan=-0.45)       # dub

# ---------- Saída (#121): carga, arrancada passando da esquerda para a direita ----------
por(zip_(0.45, 180, 520, lambda u: u * u), T['sai'], 0.05, pan=-0.6)
d = 0.65
panmov = np.linspace(-0.6, 1.0, int(d * SR))
por(sopro(d, 500, 5000, lambda u: np.clip(u / 0.12, 0, 1) * (1 - u) ** 1.5), T['sai'] + 0.45, 0.8, pan=panmov, rev=0.3)
por(baque(80, 0.3, 0.06), T['sai'] + 0.45, 0.3, pan=-0.6)

# ---------- Reverb e mixagem ----------
ir_t = tt(2.2)
ir = np.array([filtro(rng.standard_normal(len(ir_t)), 'lowpass', 5000) * np.exp(-ir_t / 0.45) for _ in range(2)])
ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
mix = seco + np.array([signal.fftconvolve(envio[c], ir[c])[:N] for c in range(2)]) * 0.9
mix = filtro(mix, 'highpass', 28)
mix = np.tanh(mix * 1.4) / 1.4                                # limitador suave
mix *= 0.89 / np.max(np.abs(mix))
wav = os.path.join(AQUI, 'sons.wav')
wavfile.write(wav, SR, (mix.T * 32767).astype(np.int16))
print('ok sons.wav')

video = os.path.join(AQUI, 'video.mp4')
final = os.path.join(AQUI, 'vinheta-adullam-com-som.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-ar', '48000', '-shortest', '-movflags', '+faststart', final], check=True)
print('ok vinheta-adullam-com-som.mp4')
