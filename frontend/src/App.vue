<template>
  <div>
    <h1>WB_Scraper</h1>
    <ProductTable ref="table" />
    <PriceHistogram :products="products" />
    <DiscountRatingChart :products="products" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import ProductTable from './components/ProductTable.vue'
import PriceHistogram from './components/PriceHistogram.vue'
import DiscountRatingChart from './components/DiscountRatingChart.vue'

const table = ref(null)
const products = ref([])

// Доступ к списку из таблицы
watch(table, () => {
  if (table.value) products.value = table.value.filteredAndSorted
})
</script>
