<template>
    <form class="form-spacing">
      <div class="row">
        <div class="text-center mb-3">
          <h1 class="display-4">Upload del dizionario dati</h1>
        </div>
        <div class="col-12">
          <div class="input-group">
            <input id="fileInput" class="form-control" type="file" accept=".sql,.json" @change="handleFileUpload"
              arial-descridedby="fileInput" arial-label="Upload">
            <button class="btn btn-outline-secondary" type="button" @click="uploadFile">Upload</button>
          </div>
          <div v-if="!isAllowed" class="alert alert-danger d-flex align-items-center" role="alert">
              <span class="fas fa-times-circle mr-2"></span>
              Per favore, seleziona un file .sql o .json
          </div>
          <div v-else class="alert alert-success d-flex align-items-center" role="alert">
                <span class="fas fa-check-circle text-success"></span>
                File pronto al caricamento
          </div>
          </div>
      </div>
      <div v-if="isLoading">Caricamento in corso...</div>
      <div class="row">
        <div class="col-12">
          <table class="table">
            <thead class="thead-light">
              <tr>
                <th scope="col">#</th>
                <th scope="col">File Name</th>
                <th scope="col">File extension</th>
                <th scope="col">Date</th>
                <th scope="col">Size</th>
                <th scope="col" colspan="2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(file, index) in files" :key="index" :class="{ 'table-success': file.loaded }">
                <th scope="row">{{ index + 1 }}</th>
                <td>
                  {{ file.name }}
                  <span v-if=file.loaded class="fas fa-check text-success ml-1"></span>
                </td>
                <td>{{ file.extension }}</td>
                <td>{{ file.date }}</td>
                <td>{{ file.size }}</td>
                <td>
                  <button type="button" class="btn btn-danger" @click="deleteFile(file.name + file.extension)">
                    <span class="fas fa-trash-alt"></span> 
                    Delete
                  </button>
                </td>
                <td>
                  <button type="button" class="btn btn-success" @click="loadSelectedFile(file)">
                    <span class="fas fa-upload"></span>
                    Load
                  </button>  
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </form>
</template>

<script>
import axios from '@/axios.js';
export default {
  data() {
    return {
      files: [],
      file: null,
      isLoading: false,
      isAllowed: false,
      loadedFile: false,
    };
  },
  computed: {
    isFileAllowed() {
      return this.file && (this.file.type === 'application/sql' || this.file.type === 'application/json');
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
      const validExtensions = ['json', 'sql'];
      const extension = this.file.name.split('.').pop();
      console.log('File extension: ', extension);

      if(validExtensions.includes(extension)) {
        this.isAllowed = true;
        console.log('File uploaded: ', this.file);
      } else {
        this.file = null;
        this.isAllowed = false;
      }
    },
    formatFileSize(size) {
      if (size < 1024) {
        return `${size} B`;
      } else if (size < 1048576) {
        return `${(size / 1024).toFixed(2)} KB`;
      } else if (size < 1073741824) {
        return `${(size / 1048576).toFixed(2)} MB`;
      } else {
        return `${(size / 1073741824).toFixed(2)} GB`;
      }
    },
    uploadFile() {
      let formData = new FormData();
      formData.append('file', this.file);
      this.isLoading = true;
      axios.post('/upload', formData)
        .then(response => {
          console.log(response)
          this.loadFiles();
          this.isLoading = false;
        }).catch(error => {
          console.log(error)
        })

    },
    loadFiles() {
      axios.get('/files').then(response => {
        this.files = response.data.map(file => {
          return {
            ...file,
            date: new Date(file.date).toLocaleString('it-IT'),
            size: this.formatFileSize(file.size)
          }
        })
      }).catch(error => {
        console.log(error)
      })
    },
  },
  mounted() {
    this.loadFiles();
  }
};
</script>

<style>
.form-spacing {
  margin-top: 100px;
}
</style>