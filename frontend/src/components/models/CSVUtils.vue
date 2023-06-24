<template>
    <div class="upload-page">
        <h2>Upload CSV File</h2>
        <label class="file-input">
            <input type="file" @change="handleFileUpload" accept=".csv" />
            <span class="nav-button">Choose File</span>
        </label>
        <div v-if="uploadedFile">
            <p>Uploaded file: {{ uploadedFile.name }}</p>
            <b-table responsive :items="csvRows" :bordered=true table-variant="secondary">
                <template #cell(selected)="row">
                    <b-button @click="updateInputFieldsFromSelected(row.item)">Copy Value</b-button>
                </template>
            </b-table>

            <div class="input-group">
                <b-form-group v-for="(column, index) in computedArray" :key="column" :label="column">
                    <b-form-input v-model="inputObject[column]" :id="column" :name="column">
                    </b-form-input>
                </b-form-group>
            </div>

            <div class="field-select">
                <b-form-checkbox v-model="bodyContainsOutputLabel">
                    Does the input body contain output label?
                </b-form-checkbox>
                <b-form-select v-if="bodyContainsOutputLabel" v-model="selectedColumn" :options="computedArray">
                    Select which column is the output label below
                </b-form-select>
                <div class="mt-3" v-if="bodyContainsOutputLabel">Selected: <strong>{{ selectedColumn }}</strong></div>
            </div>
        </div>
        <div v-else>
            <p>No file uploaded</p>
        </div>
        <button class="nav-button" @click="getPrediction">Get Prediction</button>
        <div v-if="isLoading">
            <Spinner></Spinner>
        </div>
        <div>
            {{ predictionValue }}
        </div>
    </div>
</template>
  
<script>
import { BFormInput, BFormGroup } from 'bootstrap-vue'
import {mapState, mapMutations} from 'vuex';
import Papa from 'papaparse';
import { submitData } from '../../services/api';
import Spinner from '../utils/Spinner.vue';

export default {
    name: 'CsvUpload',
    data() {
        return {
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
      uploadedFile: state => state.uploadedFile,
      csvRows: state => state.csvRows,
      csvHeaders: state => state.csvHeaders,
    }),
    computedArray() {
        const keyword = 'id';
        return this.csvHeaders.filter(item => item !== keyword);
    },
    predictionValue() {
        if (this.predictionResult !== null){
            return this.predictionResult[0];
        }
    }
  },
  components: {
    Spinner,
  },
  watch: {
    inputObject: {
        deep: true,
        handler(newVal) {
            this.convertValues(newVal);
        }
    }
  },
  methods: {
    ...mapMutations(['setUploadedFile', 'setCSVRows', 'setCSVHeaders']),
    initializeInputFields(inputObject, exampleObject) {
        for (let field in exampleObject) {
            this.$set(this.inputObject, field, '');
        }
    },
    updateInputFieldsFromSelected(selectedObject){
        for (let field in selectedObject) {
            this.inputObject[field] = selectedObject[field];
        }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: function(results) {
                    const file = event.target.files[0];
                    this.setUploadedFile(file);
                    
                    const csvContent = results.data.slice(0,5);
                    this.initializeInputFields(this.inputObject, csvContent[0]);

                    // add selected field for use with copy button
                    csvContent.forEach(
                        element => {
                            element['selected'] = false
                        }
                    );
                    this.setCSVRows(csvContent);

                    const fields = results.meta.fields;
                    this.setCSVHeaders(fields);
                }.bind(this)
            });
    },
    convertValues(inputObject) {
        console.log('handle start');
        console.log(inputObject);
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
        const excludedFields = ['id', 'selected'];
        if (this.bodyContainsOutputLabel) {
            excludedFields.push(this.selectedColumn);
        }
        const filteredObject = Object.keys(inputObject)
            .filter(key => !excludedFields.includes(key))
            .reduce((obj, key) => {
                obj[key] = inputObject[key];
                return obj;
            }, {});

        const inferenceObject = {
            feature: filteredObject
        }
        return inferenceObject;
    },
    async getPrediction() {
        const inferenceBody = this.generateInferenceBody(this.inputObject);
        console.log(inferenceBody);
        this.isLoading = true;

        try {
            const response = await submitData(inferenceBody);

            this.isLoading = false;
            const result = response.result;
            this.parseJsonData(result);
            // if (response.data.length > 0) {
            //     console.log(response.data[0]);
            // }
        } catch (error) {
            console.error(error);
            this.isLoading = false;
        }
    },
    parseJsonData(jsonString) {
      try {
        this.predictionResult = JSON.parse(jsonString);
        console.log(this.predictionResult);
      } catch (error) {
        console.error('Error parsing JSON data:', error);
      }
    }
  }}

</script>
<style scoped>
.upload-page {
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

.input-group {
    border: 1px solid #000000;
    padding: 10px;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
}

.field-select {
    padding: 10px;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
}
</style>
  