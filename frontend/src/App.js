

import {Container} from '@material-ui/core';
import Greetings from './components/Greetings';
import ScoreSlider from './components/ScoreSlider';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import InfiniteScroll from 'react-infinite-scroll-component';

const base_url = "http://localhost:8001";

function App() {
  const [uniList, setUniList] = useState([]);
  const [uniCards, setUniCards] = useState([]);
  const [cardsLoading, setCardsLoading] = useState(false);

  // get item list
  useEffect(() => {
    axios.get(base_url+"/get_list").then((resp) => {
        setUniList(resp.data);

        setCardsLoading(true);        

    }).catch(error => console.log(error));
  }, []);

  // get cards
  useEffect(() => {

    if(cardsLoading === true){
      let temp = [];
      uniList.forEach((list_item) => {
        
        axios.get(base_url+`/get_card?id=${list_item.id}`).then((resp) => {
            temp = [...temp, resp.data];
            
        }).catch(error => console.log(error));
        
      });
      setUniCards([...uniCards, ...temp]);
      setCardsLoading(false);
    }

  }, [cardsLoading]);

  return (
    <Container maxWidth="md">

      <Greetings />
      <ScoreSlider />
      {JSON.stringify(uniCards)}
      {uniCards.map( li => <p key={li.id}>{JSON.stringify(li)}</p> )}
    </Container>
    
  );
}

export default App;
