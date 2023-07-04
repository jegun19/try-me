<template>
  <div class="upload-page">
    <div class="centralized">
      <h2>Upload CSV File</h2>
      <label class="file-input">
        <input type="file" @change="handleFileUpload" accept=".csv" />
        <b-button variant="primary">Choose File</b-button>
      </label>
    </div>
    <div v-if="uploadedFile">
      <h3>Uploaded Filename: {{ uploadedFile.name }}</h3>
      <div class="table-container">
        <b-table
          responsive
          :items="csvRows"
          :bordered="true"
          table-variant="secondary"
        >
          <template #cell(selected)="row">
            <b-button
              variant="primary"
              @click="updateInputFieldsFromSelected(row.item)"
              >Copy Value</b-button
            >
          </template>
        </b-table>
      </div>

      <div class="input-group">
        <b-form-group
          v-for="(column, index) in computedArray"
          :key="column"
          :label="column"
          :invalid-feedback="invalidFeedback"
        >
          <b-form-input
            v-model="inputObject[column]"
            :state="inputFieldsState(column)"
            :invalid-feedback="invalidFeedback"
            :id="column"
            :name="column"
          >
          </b-form-input>
        </b-form-group>
      </div>

      <div class="field-select">
        <b-form-checkbox v-model="bodyContainsOutputLabel">
          Does the input body contain output label?
        </b-form-checkbox>
        <b-form-select
          v-if="bodyContainsOutputLabel"
          v-model="selectedColumn"
          :options="computedArray"
        >
          Select which column is the output label below
        </b-form-select>
        <div class="mt-3" v-if="bodyContainsOutputLabel">
          Selected: <strong>{{ selectedColumn }}</strong>
        </div>
      </div>
    </div>
    <div class="centralized">
      <b-button
        v-b-modal.modal-1
        :variant="buttonVariant"
        size="lg"
        :disabled="areAllInputFieldsEmpty"
      >
        Get Prediction
      </b-button>
      <b-modal
        id="modal-1"
        title="Confirmation Pop-up Dialog"
        @ok="getPrediction"
      >
        <p class="my-4">{{ popupConfirmationDialog }}</p>
      </b-modal>
      <div v-if="isLoading">
        <Spinner></Spinner>
      </div>
      <div class="number-widget" v-if="predictionResult">
        <span class="text"> Result: </span>
        <span class="number"> {{ predictionValue }} </span>
      </div>
    </div>
  </div>
</template>

<script>
import { BFormInput, BFormGroup } from "bootstrap-vue";
import { mapState, mapMutations } from "vuex";
import Papa from "papaparse";
import { submitData } from "../../services/api";
import Spinner from "../utils/Spinner.vue";

export default {
  name: "CsvUpload",
  data() {
    return {
      showDialog: false,
      buttonVariant: "secondary",
      parsed: false,
      inputFields: [],
      inputObject: {},
      bodyContainsOutputLabel: null,
      selectedColumn: null,
      isLoading: false,
      predictionResult: null,
    };
  },
  computed: {
    ...mapState({
      uploadedFile: (state) => state.uploadedFile,
      csvRows: (state) => state.csvRows,
      csvHeaders: (state) => state.csvHeaders,
    }),
    computedArray() {
      const keyword = "id";
      return this.csvHeaders.filter((item) => item !== keyword);
    },
    predictionValue() {
      if (this.predictionResult !== null) {
        return this.predictionResult[0].data;
      }
    },
    invalidFeedback() {
      return "Please enter a value";
    },
    popupConfirmationDialog() {
      if (this.bodyContainsOutputLabel) {
        return (
          "You have selected " +
          this.selectedColumn +
          " column to be excluded from prediction. Press OK to continue or press cancel to modify your selection"
        );
      } else {
        return "Are you sure? If yes, press OK to continue";
      }
    },
    areAllInputFieldsEmpty() {
      // avoid returning false when inputObject is not initialized
      if (Object.keys(this.inputObject).length === 0) {
        return true;
      }
      for (const field in this.inputObject) {
        if (this.inputObject[field] === "") {
          return true;
        }
      }
      return false;
    },
  },
  components: {
    Spinner,
  },
  watch: {
    inputObject: {
      deep: true,
      handler(newVal) {
        this.convertValues(newVal);
      },
    },
    areAllInputFieldsEmpty: {
      handler(newVal) {
        if (newVal) {
          this.buttonVariant = "secondary";
        } else {
          this.buttonVariant = "primary";
        }
      },
    },
  },
  methods: {
    ...mapMutations(["setUploadedFile", "setCSVRows", "setCSVHeaders"]),
    initializeInputFields(inputObject, exampleObject) {
      for (let field in exampleObject) {
        this.$set(this.inputObject, field, "");
      }
    },
    updateInputFieldsFromSelected(selectedObject) {
      for (let field in selectedObject) {
        this.inputObject[field] = selectedObject[field];
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: function (results) {
          const file = event.target.files[0];
          this.setUploadedFile(file);

          const csvContent = results.data.slice(0, 5);
          this.initializeInputFields(this.inputObject, csvContent[0]);

          // add selected field for use with copy button
          csvContent.forEach((element) => {
            element["selected"] = false;
          });
          this.setCSVRows(csvContent);

          const fields = results.meta.fields;
          this.setCSVHeaders(fields);
        }.bind(this),
      });
    },
    convertValues(inputObject) {
      for (const key in inputObject) {
        if (Object.prototype.hasOwnProperty.call(inputObject, key)) {
          const value = inputObject[key];
          if (/^\d+$/.test(value)) {
            inputObject[key] = parseInt(value, 10); // Convert to integer
          } else if (/^\d+(\.\d+)?$/.test(value)) {
            inputObject[key] = parseFloat(value); // convert to float
          }
          // No need to convert if it's not a number (treat as string)
        }
      }
    },
    generateInferenceBody(inputObject) {
      const excludedFields = ["id", "selected"];
      if (this.bodyContainsOutputLabel) {
        excludedFields.push(this.selectedColumn);
      }
      const filteredObject = Object.keys(inputObject)
        .filter((key) => !excludedFields.includes(key))
        .reduce((obj, key) => {
          obj[key] = inputObject[key];
          return obj;
        }, {});

      const inferenceObject = {
        feature: filteredObject,
      };
      return inferenceObject;
    },
    async getPrediction() {
      const inferenceBody = this.generateInferenceBody(this.inputObject);
      this.isLoading = true;

      try {
        const response = await submitData(inferenceBody);

        this.isLoading = false;
        const result = response.result;
        this.parseJsonData(result);
      } catch (error) {
        console.error(error);
        this.isLoading = false;
      }
    },
    parseJsonData(jsonString) {
      try {
        this.predictionResult = JSON.parse(jsonString);
      } catch (error) {
        console.error("Error parsing JSON data:", error);
      }
    },
    inputFieldsState(colName) {
      const isFieldEmpty = this.inputObject[colName] === "";
      return !isFieldEmpty;
    },
  },
};
</script>
<style>
/* Remove square border around close button in b-modal */
.modal-header button.close {
  border: none;
  outline: none;
  background: transparent;
  padding: 0;
}

.upload-page {
  margin-top: 2rem;
  padding-top: 20px;
}

.centralized {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
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

.table-container {
  width: 100%;
  max-width: 1200px; /* Adjust the maximum width as needed */
  overflow-x: auto;
}

.input-group {
  border: 1px solid #000000;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  margin-bottom: 10px;
}

.field-select {
  border: 1px solid #000000;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  margin-bottom: 10px;
}
.number-widget {
  display: inline-block;
  font-size: 24px;
  padding: 5px;
  margin-top: 20px;
  margin-left: 5px;
}
.number-widget .number {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px;
  margin-left: 5px;
}
.number-widget .text {
  font-weight: bold;
}

.modal-content {
  color: black;
}
</style>
