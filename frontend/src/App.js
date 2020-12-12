
import './App.css';
import { Button, Container } from '@material-ui/core';
import Greetings from './components/Greetings'

function App() {
  return (
    <Container maxWidth="sm">
      <Greetings />
      <Button color="primary">Hello World</Button>
    </Container>
    
  );
}

export default App;
