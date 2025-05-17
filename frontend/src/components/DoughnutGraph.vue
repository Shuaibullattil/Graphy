<template>
  <div>
    <Doughnut v-if="chartData" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import { Doughnut } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

export default {
  name: 'DoughnutChart',
  components: { Doughnut },
  props: {
    title: {
      type: String,
      default: 'Default Doughnut Chart',
    },
    jsonUrl: {
      type: [String, Array],
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
    };
  },
  methods: {
    isMostlyString(arr) {
      const stringCount = arr.filter(v => typeof v === 'string').length;
      return stringCount / arr.length > 0.8;
    },
    isMostlyNumber(arr) {
      const numberCount = arr.filter(v => typeof v === 'number' && !isNaN(v)).length;
      return numberCount / arr.length > 0.8;
    },
    async loadChartData() {
      try {
        let rawData;

        if (typeof this.jsonUrl === 'string') {
          const response = await fetch(this.jsonUrl);
          rawData = await response.json();
        } else if (Array.isArray(this.jsonUrl)) {
          rawData = this.jsonUrl;
        } else {
          throw new Error('Invalid jsonUrl type');
        }

        if (!rawData.length) throw new Error('Empty data');

        const keys = Object.keys(rawData[0]);

        // Build columns
        const columns = {};
        keys.forEach(k => {
          columns[k] = rawData.map(item => item[k]);
        });

        // Detect label and value columns
        let labelKey = keys.find(k => this.isMostlyString(columns[k]));
        let valueKey = keys.find(k => this.isMostlyNumber(columns[k]));

        if (!labelKey) labelKey = keys[0];
        if (!valueKey) valueKey = keys.find(k => k !== labelKey) || keys[1];

        const labels = rawData.map(item => item[labelKey] ?? 'Unknown');
        const values = rawData.map(item => {
          const val = Number(item[valueKey]);
          return isNaN(val) ? 0 : val;
        });

        const backgroundColors = labels.map(() => {
          const hue = Math.floor(Math.random() * 30) + 90;
          const saturation = Math.floor(Math.random() * 20) + 60;
          const lightness = Math.floor(Math.random() * 30) + 40;
          return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
        });

        this.chartData = {
          labels,
          datasets: [
            {
              label: valueKey,
              data: values,
              backgroundColor: backgroundColors,
              borderColor: '#fff',
              borderWidth: 1,
            },
          ],
        };

        this.chartOptions.plugins.title.text = this.title;
      } catch (error) {
        console.error('Error loading or processing data:', error);
      }
    },
  },
  watch: {
    jsonUrl: {
      handler() {
        this.loadChartData();
      },
      immediate: true,
      deep: true,
    },
  },
};
</script>

<style scoped>
div {
  height: 300px;
}
</style>
