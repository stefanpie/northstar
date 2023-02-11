<template>
  <div class="color-test-grid">
    <!-- 
    --ct-primary: var(--color-blue-500);
    --ct-secondary: #6c757d;
    --ct-success: #28a745;
    --ct-info: #17a2b8;
    --ct-warning: #ffc107;
    --ct-danger: #dc3545;
    --ct-light: #f8f9fa;
    --ct-dark: #343a40;
    --ct-white: #fff;
    --ct-black: #000;
    -->
    <div class="color-test-grid-primary"></div>
    <div class="color-test-grid-secondary"></div>
    <div class="color-test-grid-border"></div>
    <div class="color-test-grid-success"></div>
    <div class="color-test-grid-info"></div>
    <div class="color-test-grid-warning"></div>
    <div class="color-test-grid-danger"></div>
    <div class="color-test-grid-light"></div>
    <div class="color-test-grid-dark"></div>
    <div class="color-test-grid-white"></div>
    <div class="color-test-grid-black"></div>
  </div>
</template>

<script setup></script>

<style scoped>
.color-test-grid {
  grid-gap: 1rem;
  display: grid;
  grid-template-rows: repeat(2, 1fr);
  grid-template-columns: repeat(5, 1fr);
  padding: 1rem;
  width: 100%;
  height: 100%;
}

.color-test-grid-primary {
  background-color: var(--ct-primary);
}

.color-test-grid-secondary {
  background-color: var(--ct-secondary);
}

.color-test-grid-border {
  background-color: var(--ct-border);
}

.color-test-grid-success {
  background-color: var(--ct-success);
}

.color-test-grid-info {
  background-color: var(--ct-info);
}

.color-test-grid-warning {
  background-color: var(--ct-warning);
}

.color-test-grid-danger {
  background-color: var(--ct-danger);
}

.color-test-grid-light {
  background-color: var(--ct-light);
}

.color-test-grid-dark {
  background-color: var(--ct-dark);
}

.color-test-grid-white {
  background-color: var(--ct-white);
}

.color-test-grid-black {
  background-color: var(--ct-black);
}
</style>
