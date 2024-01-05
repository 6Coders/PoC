<template>
    <form>
      <div id="app" class="container mt-5">
        <div class="text-center mb-3">
          <h1 class="display-4">Generatore di Prompt</h1>
        </div>
        <div class="mb-3">
          <label for="inputText" class="form-label">Inserisci qui la tua richiesta:</label>
          <input  type="text" class="form-control" id="inputPrompt">
        </div>
        <div class="mb-3">
          <label class="form-label">File caricato: nome del db</label>
        </div>
        <button type="submit"  class="btn btn-primary">Genera Prompt</button>
        <div class="mt-5">
          <label for="generatedPrompt" class="form-label">Prompt Generato:</label>
          <textarea class="form-control" id="generatedPrompt" readonly></textarea>
        </div>
        <button class="btn btn-dark float-end mt-5" @click="redirectToAccessPage()">Torna alla scelta utente</button>
      </div>
    </form>
    </template>
    
    <script>
    export default {
      methods: {
        redirectToAccessPage() {
          this.$router.push({ name: 'home' });
        }
      }
    };
    </script>