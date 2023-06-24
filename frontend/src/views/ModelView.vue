<template>
  <div>
    <h1>Upload Model and Input Sample</h1>
    <ModelUpload />
    <CsvUpload />
  </div>
</template>
  
<script>
  import CsvUpload from '../components/models/CSVUtils.vue';
  import ModelUpload from '../components/models/ModelUpload.vue';
  
  export default {
    components: {
    CsvUpload,
    ModelUpload
},
  };
  </script>
