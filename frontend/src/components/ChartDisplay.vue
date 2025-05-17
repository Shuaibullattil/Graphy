<template>
  <div v-if="chartData">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  rawData: Array
})

const chartData = {
  labels: props.rawData.map(item => item.Category), // X-axis (change to your column)
  datasets: [
    {
      label: 'Amount', // Y-axis
      data: props.rawData.map(item => item.Amount), // Change keys based on your Excel
      backgroundColor: 'rgba(75, 192, 192, 0.7)'
    }
  ]
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'Data Chart'
    }
  }
}
</script>
