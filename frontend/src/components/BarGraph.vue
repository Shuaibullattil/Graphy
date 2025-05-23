<template>
  <div>
    <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
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
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import { generateOrderedShades } from '@/utils/colour.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default {
  name: 'BarGraph',
  components: { Bar },
  props: {
    title: {
      type: String,
      default: 'Default Bar Chart',
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

        // Build columns: key -> array of values
        const columns = {};
        keys.forEach((k) => {
          columns[k] = rawData.map(item => item[k]);
        });

        // Find label column: mostly strings
        let labelKey = keys.find(k => this.isMostlyString(columns[k]));

        // Find value column: mostly numbers
        let valueKey = keys.find(k => this.isMostlyNumber(columns[k]));

        // Fallback to first columns if detection fails
        if (!labelKey) labelKey = keys[0];
        if (!valueKey) valueKey = keys.find(k => k !== labelKey) || keys[1];

        // Prepare labels and values arrays
        const labels = rawData.map(item => item[labelKey] ?? 'Unknown');
        const values = rawData.map(item => {
          const val = Number(item[valueKey]);
          return isNaN(val) ? 0 : val;
        });

        // // Generate background colors
        // const backgroundColors = labels.map(() => {
        //     const hue = Math.floor(Math.random() * 360); // Full color spectrum
        //     const saturation = Math.floor(Math.random() * 30) + 70; // 70% to 100%
        //     const lightness = Math.floor(Math.random() * 20) + 45; // 45% to 65%
        //     return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
        //     });



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
