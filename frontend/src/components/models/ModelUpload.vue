<template>
  <div class="model-upload-page">
    <h2>Upload Model File</h2>
    <div class="button-container">
      <label class="file-input">
        <input type="file" @change="uploadModel" ref="modelFile" />
        <b-button class="button" variant="primary">Select Model File</b-button>
      </label>
      <b-button
        class="button"
        v-if="isFileSelected"
        variant="primary"
        @click="submitFile"
      >
        Upload
      </b-button>
    </div>
  </div>
</template>

<script>
import { uploadModel } from "../../services/api";

export default {
  data() {
    return {
      modelFile: null,
    };
  },
  computed: {
    isFileSelected() {
      return this.modelFile !== null;
    },
  },
  methods: {
    uploadModel() {
      this.modelFile = this.$refs.modelFile.files[0];
      console.log(this.modelFile);
    },
    async submitFile() {
      const formData = new FormData();
      formData.append("file", this.modelFile);

      try {
        const response = await uploadModel(formData);
        console.log(response);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.model-upload-page {
  margin-top: 2rem;
}

.nav-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: lightgreen;
  /* Set the desired light green color */
  color: white;
  /* Set the text color to white */
  border: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s;
  cursor: pointer;
}

.nav-button:hover {
  background-color: lightgreen;
  /* Set the same light green color on hover */
  opacity: 0.8;
  /* Optional: Reduce the opacity on hover for a subtle effect */
}

.file-input {
  position: relative;
  display: inline-block;
}

.file-input input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.button-container {
  display: flex;
}

.button {
  margin-right: 10px;
}
</style>
