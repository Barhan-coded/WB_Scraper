<template>
    <div>
      <!-- Фильтры -->
      <div class="filters">
        <label>Цена: 
          <input type="range" v-model="priceRange[0]" :min="minPrice" :max="maxPrice" />
          <input type="range" v-model="priceRange[1]" :min="minPrice" :max="maxPrice" />
          {{ priceRange[0] }}–{{ priceRange[1] }}
        </label>
        <label>Мин. рейтинг:
          <input type="number" v-model="minRating" step="0.1" min="0" max="5" />
        </label>
        <label>Мин. отзывов:
          <input type="number" v-model="minReviews" step="1" min="0" />
        </label>
        <label>Сортировать по:
          <select v-model="sortField">
            <option value="name">Название</option>
            <option value="price">Цена</option>
            <option value="rating">Рейтинг</option>
            <option value="review_count">Отзывы</option>
          </select>
          <button @click="sortAsc = !sortAsc">
            {{ sortAsc ? '↑' : '↓' }}
          </button>
        </label>
      </div>
  
      <!-- Таблица -->
      <table>
        <thead>
          <tr>
            <th>Название</th>
            <th>Цена</th>
            <th>Цена со скидкой</th>
            <th>Рейтинг</th>
            <th>Отзывы</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredAndSorted" :key="p.id">
            <td>{{ p.name }}</td>
            <td>{{ p.price }}</td>
            <td>{{ p.discounted_price || '-' }}</td>
            <td>{{ p.rating || '-' }}</td>
            <td>{{ p.review_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>
  
<script setup>
import { ref, onMounted, computed, watch, getCurrentInstance } from 'vue'
import debounce from 'lodash/debounce'

const products = ref([])
const minPrice = ref(0)
const maxPrice = ref(20000)
const priceRange = ref([minPrice.value, maxPrice.value])
const minRating = ref(0)
const minReviews = ref(0)
const sortField = ref('rating')
const sortAsc = ref(false)


const isInitial = ref(true)

// Загрузка данных
async function fetchData() {
    const api = getCurrentInstance().appContext.config.globalProperties.$api

    // передаём фильтры серверу, если хотим серверную фильтрацию:
    const params = {
        min_price: priceRange.value[0],
        max_price: priceRange.value[1],
        min_rating: minRating.value,
        min_reviews: minReviews.value
    }
    const { data } = await getCurrentInstance().appContext.config.globalProperties.$api.get('/products/', { params })
    products.value = data
    // обновляем границы слайдера при первой загрузке:
    if (isInitial.value && data.length) {
        // устанавливаем границы только при первой загрузке
        const prices = data.map(p => p.price)
        minPrice.value   = Math.min(...prices)
        maxPrice.value   = Math.max(...prices)
        priceRange.value = [minPrice.value, maxPrice.value]
        isInitial.value = false
    }
}

const debouncedFetch = debounce(fetchData, 1000)

// Перезапрос при изменении фильтров
//   watch([priceRange, minRating, minReviews], fetchData, { deep: true })
watch(
() => [priceRange.value[0], priceRange.value[1], minRating.value, minReviews.value],
debouncedFetch
)

onMounted(fetchData)

// Клиентская сортировка
const filteredAndSorted = computed(() => {
return [...products.value]
    .sort((a, b) => {
    const dir = sortAsc.value ? 1 : -1
    if (a[sortField.value] < b[sortField.value]) return -1 * dir
    if (a[sortField.value] > b[sortField.value]) return 1 * dir
    return 0
    })
})
</script>

<style scoped>
.filters { display: flex; gap: 1rem; margin-bottom: 1rem; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: .5rem; border: 1px solid #ccc; }
</style>
