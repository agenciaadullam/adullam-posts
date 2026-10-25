import {Composition} from 'remotion';
import {Teste} from './Teste';
import {QuemGoverna, DURACAO} from './QuemGoverna';
import {QuemGovernaVoz, DURACAO_VOZ} from './QuemGovernaVoz';

export const Root = () => (
  <>
    <Composition id="Teste" component={Teste} durationInFrames={60} fps={30} width={1080} height={1920} />
    <Composition id="QuemGoverna" component={QuemGoverna} durationInFrames={DURACAO} fps={30} width={1080} height={1920} />
    <Composition id="QuemGovernaVoz" component={QuemGovernaVoz} durationInFrames={DURACAO_VOZ} fps={30} width={1080} height={1920} />
  </>
);
