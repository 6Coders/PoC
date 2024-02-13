<template>
    <div id="app" class="container mt-6">
        <div class="row">
            <div class="col-md-6">
                <h1 class="display-2">Benvenuto</h1>
                <h2 class="text-body-secondary mb-5">Che tipo di utente sei?</h2>
                <div>
                    <button type="button" class="btn btn-primary custom-color btn-lg btn-block d-block mb-5" @click="redirectToManagerPage">Gestione Dizionari</button>
                    <button type="button" class="btn btn-primary custom-color btn-lg btn-block d-block" @click="redirectToUserPage">Generazione Prompt</button>
                </div>
            </div>
            <div class="col-md-2">
            </div>
            <div class="col-md-4">
                <img src="../assets/6Coders-logo.png" alt="Descrizione dell'immagine" class="img-fluid">
           </div>
        </div>
    </div>
</template>
    
<script>
    export default {
      methods: {
        redirectToManagerPage() {
          this.$router.push({ name: 'Manager' });
        },
        redirectToUserPage() {
          this.$router.push({ name: 'User' });
        }
      }
    };
</script>