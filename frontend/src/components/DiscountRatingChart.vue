<template>
    <!-- <Line :chart-data="chartData" /> -->
    <Bar :data="chartData" :options="chartOptions" />
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { Line } from 'vue-chartjs'
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
  
  // По оси X — скидка (price - discounted_price), Y — рейтинг
  const chartData = computed(() => {
    const labels = props.products.map((p, i) => `#${i+1}`)
    const discounts = props.products.map(p => p.price - (p.discounted_price || p.price))
    const ratings = props.products.map(p => p.rating || 0)
    return {
      labels,
      datasets: [
        { label: 'Скидка', data: discounts, yAxisID: 'y1' },
        { label: 'Рейтинг', data: ratings, yAxisID: 'y2' }
      ]
    }
  })
  </script>
  