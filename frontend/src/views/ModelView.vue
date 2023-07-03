<template>
  <div class="model-view">
    <h1>Upload Model and Input Sample</h1>
    <span
      >Please upload the ML model file (e.g., JSON format for XGBoost) and the
      sample input file (e.g., train.csv or test.csv)</span
    >
    <ModelUpload />
    <CsvUpload />
  </div>
</template>

<script>
import CsvUpload from "../components/models/CSVUtils.vue";
import ModelUpload from "../components/models/ModelUpload.vue";

export default {
  components: {
    CsvUpload,
    ModelUpload,
  },
};
</script>

<style scoped>
.model-view {
  display: flex;
  margin-top: 2rem;
  flex-direction: column;
  align-items: center;
}
</style>
