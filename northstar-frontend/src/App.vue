<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="top-wrapper">
    <header>
      <h1>Northstar</h1>
      <img src="" alt="" />
    </header>

    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>

    <RouterView class="main-view" />
  </div>
</template>
<style>
.top-wrapper {
  display: grid;
  grid-template-rows: 4rem 1fr;
  grid-template-columns: 12em 1fr;
  width: 100%;
  height: 100%;
}

header {
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: auto auto 1fr auto;
  grid-template-areas: 'title logo spacer';
  grid-row: 1 / 2;
  grid-column: 1 / 3;
  border-bottom: var(--bw) var(--bs) var(--ct-border);
  background-color: var(--color-color-secondary);
  padding: 0.1rem;
  padding-right: 1rem;
  padding-left: 1rem;
}

header > h1 {
  grid-area: title;
  margin: auto;
  padding: 0;
}

header .spacer {
  grid-area: spacer;
}

nav {
  display: flex;
  grid-row: 2 / 3;
  grid-column: 1 / 2;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  border-right: var(--bw) var(--bs) var(--ct-border);
  background-color: var(--color-color-secondary);
  padding-top: 1rem;
  padding-right: 1rem;
  padding-left: 1rem;
}
nav > a {
  transition: background-color 0.05s ease-in-out;
  margin-bottom: 0.5rem;
  border: var(--bw) var(--bs) var(--ct-border);
  background-color: var(--ct-primary);
  padding: 0.2rem 0.5rem;
  width: 100%;
  font-size: 1.2rem;
  user-select: none;
  text-decoration: none;
}
nav > a:hover,
nav > a.router-link-exact-active {
  border-color: var(--ct-border);
  background-color: var(--ct-secondary);
}

.main-view {
  width: 100%;
  height: 100%;
  grid-row: 2 / 3;
  grid-column: 2 / 3;
  background-color: var(--ct-primary);
  padding: 2rem;
}
</style>
