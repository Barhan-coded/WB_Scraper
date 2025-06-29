<template>
    <!-- <Bar :chart-data="chartData" /> -->
    <Bar :data="chartData" :options="chartOptions" />
  </template>
  
  <script setup>
  import { computed, watch } from 'vue'
  import { Bar } from 'vue-chartjs'
//   import Chart from 'chart.js/auto'
import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js'

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale
)

  
  const props = defineProps({
    products: Array
  })
  
  // Группировка по диапазонам цен
  const chartData = computed(() => {
    const bins = [0, 1000, 5000, 10000, 20000]
    const counts = bins.map(() => 0)
    props.products.forEach(p => {
      const price = p.price
      for (let i = 0; i < bins.length; i++) {
        if (price <= bins[i]) { counts[i]++; break }
      }
    })
    return {
      labels: bins.map(b => `≤${b}`),
      datasets: [{ label: 'Число товаров', data: counts }]
    }
  })
  
  // Перерисовка при изменении products
  watch(props.products, () => {}, { deep: true })
  </script>
  