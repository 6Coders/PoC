<template>
    <form @submit.prevent="generaPrompt">
      <div id="app" class="container mt-5">
        <div class="text-center mb-3">
          <h1 class="display-4">Generatore di Prompt</h1>
        </div>
        <div class="mb-3">
          <label for="inputText" class="form-label">Inserisci qui la tua richiesta:</label>
          <input v-model="userRequest" type="text" class="form-control" id="inputPrompt">
        </div>
        <div class="mb-3">
          <label for="loadedFile" class="form-label">File caricato: {{ loadedFile }}</label>
        </div>
        <button type="submit"  class="btn btn-primary">Genera Prompt</button>
        <div class="mt-5">
          <label for="generatedPrompt" class="form-label">Prompt Generato:</label>
          <textarea class="form-control" id="generatedPrompt" v-model="generatedPrompt" readonly></textarea>
        </div>
        <button class="btn btn-dark float-end mt-5" @click="redirectToAccessPage">Torna alla scelta utente</button>
      </div>
    </form>
    </template>
    
    <script>
    import axios from '@/axios.js';
    export default {
  data() {
    return {
      userRequest: '' ,
      generatedPrompt: '',
      loadedFile: ''
    };
  },
      methods: {
        loadFile(){
      axios.get('/getfileloaded')
        .then(response => {
          this.loadedFile = response.data.loaded;
          console.log(response.data);
        })
        .catch(error => {
          // Gestisci eventuali errori
          console.error(error);
        });
        },
        generaPrompt() {
          // Invia il testo dell'utente al backend quando il pulsante è premuto
          axios.post('/generateprompt', { userRequest: this.userRequest })
            .then(response => {
              this.generatedPrompt = response.data.result;
              console.log(response.data);
            })
            .catch(error => {
              // Gestisci eventuali errori
              console.error(error);
            });
        },
        redirectToAccessPage() {
          this.$router.push({ name: 'home' });
        }
      },
  mounted() {
    this.loadFile();
  }
    };
    </script>
