// store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    uploadedFile: null,
    csvRows: [],
    csvHeaders: [],
  },
  mutations: {
    setUploadedFile(state, file) {
      state.uploadedFile = file;
    },
    setCSVRows(state, rows) {
        state.csvRows = rows;
    },
    setCSVHeaders(state, headers) {
        state.csvHeaders = headers;
    }
  },
});
