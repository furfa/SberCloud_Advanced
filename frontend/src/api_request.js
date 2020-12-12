import axios from 'axios';

const base_url = "http://192.168.105.87:8001";

export const get_list = (setAppState) =>{
    axios.get(base_url+"/get_list").then((resp) => {
        setAppState(resp.data);
        console.log(resp.data);
    });
}

export const get_card = (id) =>{
    axios.get(base_url+"/get_card?id="+String(id) ).then((resp) => {
        console.log(resp.data);
    });
}