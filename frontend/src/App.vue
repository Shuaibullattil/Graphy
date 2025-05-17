<template>
  <div class="p-6">
    <h1 class="text-2xl mb-4">📊 Excel to Graph Visualizer</h1>
    <FileUpload @dataParsed="onDataParsed" />
    <p v-if="parsedData">{{ parsedData }}</p>
    <p v-else>sorry no data</p>
    <ChartDisplay v-if="parsedData.length" :rawData="parsedData" />
  </div>
</template>

<script setup>
import FileUpload from './components/FileUpload.vue'
import ChartDisplay from './components/ChartDisplay.vue'
import { ref } from 'vue'

const parsedData = ref([])

const onDataParsed = (data) => {
  parsedData.value = data
}
</script>
