<template>
  <div class="landing-page">
    <section class="hero">
      <h1>Turn Your Excel into Beautiful Charts</h1>
      <p>
        Upload your Excel or CSV files and instantly visualize your data with bar, pie, and doughnut charts.
        Simple. Fast. Elegant.
      </p>
      <button class="cta-button" @click="navigateToConvert">TRY NOW</button>
    </section>

    <section class="charts">
      <div class="chart-container" v-for="(chart, index) in chartComponents" :key="index">
        <component
          :is="chart.component"
          :chart-data="chart.data"
          :chart-options="chart.options"
          style="height: 100%; width: 100%;"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { Bar, Pie, Doughnut } from 'vue-chartjs'
import { useRouter } from 'vue-router'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale)

const router = useRouter()

const navigateToConvert = () => {
  router.push('/convert')
}

const sampleData = {
  labels: ['A', 'B', 'C', 'D'],
  datasets: [
    {
      label: 'Sample Data',
      backgroundColor: ['#a78bfa', '#c084fc', '#d8b4fe', '#f0abfc'],
      data: [40, 20, 10, 30],
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}

const chartComponents = [
  { component: Bar, data: sampleData, options: chartOptions },
  { component: Pie, data: sampleData, options: chartOptions },
  { component: Doughnut, data: sampleData, options: chartOptions }
]
</script>

<style scoped>
.landing-page {
  background: linear-gradient(to bottom right, #a78bfa, #c084fc);
  min-height: 100vh;
  padding: 2rem;
  color: white;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero {
  text-align: center;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-inline: auto;
}

.cta-button {
  background-color: white;
  color: #9333ea;
  padding: 0.75rem 2rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 1.1rem;
  text-decoration: none;
  transition: background-color 0.3s;
}

.cta-button:hover {
  background-color: #f3e8ff;
}

.charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  width: 100%;
  max-width: 1000px;
  padding: 1rem;
}

.chart-container {
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 1rem;
  padding: 1rem;
  height: 300px;
}
</style>
