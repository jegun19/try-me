<template>
  <div id="app">
    <header>
      <div class="wrapper">
        <h1 class="title">Project TryMe</h1>
        <nav>
          <router-link to="/" class="nav-button">About</router-link>
          <router-link to="/model" class="nav-button">Model</router-link>
        </nav>
      </div>
    </header>

    <router-view />
  </div>
</template>

<style scoped>
.nav-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #a2e8b7;
  color: #047d52;
  text-decoration: none;
  margin-right: 1rem;
  transition: background-color 0.3s ease;
}

.nav-button:hover {
  background-color: #c3f4d4;
}

.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
