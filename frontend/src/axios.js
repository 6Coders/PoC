import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:5000' //su docker cambiare la porta in 8000
});

export default instance;