<template>
  <div>
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    <p v-else>Loading chart...</p>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import { generateOrderedShades } from '@/utils/colour.js'

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend)

export default {
  name: 'BarGraph',
  components: { Bar },
  props: {
    title: {
      type: String,
      default: 'Default Bar Chart',
    },
    chartInput: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartData: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: true,
            text: this.title,
          },
        },
      },
    }
  },
  methods: {
    isMostlyString(arr) {
      const stringCount = arr.filter(v => typeof v === 'string').length
      return stringCount / arr.length > 0.8
    },
    isMostlyNumber(arr) {
      const numberCount = arr.filter(v => typeof v === 'number' && !isNaN(v)).length
      return numberCount / arr.length > 0.8
    },
    processData(data) {
      if (!Array.isArray(data) || data.length === 0) {
        throw new Error('Empty or invalid data')
      }

      const keys = Object.keys(data[0])
      const columns = {}
      keys.forEach(k => {
        columns[k] = data.map(item => item[k])
      })

      let labelKey = keys.find(k => this.isMostlyString(columns[k]))
      let valueKey = keys.find(k => this.isMostlyNumber(columns[k]))

      if (!labelKey) labelKey = keys[0]
      if (!valueKey) valueKey = keys.find(k => k !== labelKey) || keys[1]

      const labels = data.map(item => item[labelKey] ?? 'Unknown')
      const values = data.map(item => {
        const val = Number(item[valueKey])
        return isNaN(val) ? 0 : val
      })

      this.chartData = {
        labels,
        datasets: [
          {
            label: valueKey,
            data: values,
            backgroundColor: generateOrderedShades(labels),
            borderColor: generateOrderedShades(labels),
            borderWidth: 1,
          },
        ],
      }
    },
  },
  watch: {
    chartInput: {
      handler(newVal) {
        try {
          this.processData(newVal)
        } catch (err) {
          console.error('Error processing data:', err)
          this.chartData = null
        }
      },
      immediate: true,
      deep: true,
    },
  },
}
</script>

<style scoped>
div {
  height: 300px;
}
</style>
