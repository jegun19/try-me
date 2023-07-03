<template>
  <div class="page">
    <header>
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
      />
    </header>

    <main>
      <section id="about">
        <div class="container">
          <h2>About</h2>
          <p>
            This tool is a web platform designed for business teams and product
            managers to perform inference on a machine learning model. It
            automates the creation of input fields based on an example CSV file,
            allowing users to easily provide input values for each column.
          </p>

          <h3>Instructions</h3>
          <ol class="instructions">
            <li>
              <i class="fas fa-upload"></i>
              Upload the saved machine learning model file in the form of a JSON
              file.
            </li>
            <li>
              <i class="fas fa-upload"></i>
              Upload a CSV file containing the example data used to train the
              machine learning model.
            </li>
            <li>
              <i class="fas fa-cogs"></i>
              The tool will automatically generate an input field for each
              column in the CSV file.
            </li>
            <li>
              <i class="fas fa-pencil-alt"></i>Fill in the input values for each
              column accordingly.
            </li>
            <li>
              <i class="fas fa-play"></i>
              Click on the prediction button.
            </li>
            <li>
              <i class="fas fa-exchange-alt"></i>The platform will generate the
              JSON data based on the data schema and send an HTTP POST request
              to the backend for inference. It will then return the prediction
              result.
            </li>
            <li>
              <i class="fas fa-chart-line"></i>Upon success, the prediction
              result will be returned.
            </li>
          </ol>
        </div>
      </section>
    </main>
    <footer>
      <div class="container">
        <p>&copy; 2023 TryMe. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  padding-top: 20px; /* Adjust the top padding as needed */
}

.instructions {
  text-align: left;
}

.container {
  max-width: 800px;
  padding: 40px;
  text-align: center;
}

h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

h3 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

ol {
  margin-left: 20px;
  margin-bottom: 20px;
}

li {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 10px;
}

footer {
  background-color: #f0f0f0;
  padding: 20px 0;
}

footer p {
  font-size: 14px;
  color: #666;
  margin: 0;
}
</style>
