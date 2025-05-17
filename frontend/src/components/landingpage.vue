// LandingPage.vue
<template>
  <div>
    <h1>Landing Page</h1>
    <button @click="$router.push('/pageone')">Go to Page One</button>
    <button @click="$router.push('/pagetwo')">Go to Page Two</button>
    <button @click="$router.push('/pagethree')">Go to Page Three</button>
    <FileUpload @dataParsed="datainJSON"/>
    <p v-if="graphData.length > 0">Data loaded successfully</p>
    <div class="gridforGraph">
        <div class="box">
            <DownloadChart :chartRef="bargraphref" filename="bar_graph.png"/>
            <div ref="bargraphref">
                <BarGraph title="Bargraph" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/>
            </div>
            
        </div>
        <div class="box">
            <DownloadChart :chartRef="doughnutref" filename="doughnut_graph.png"/> 
            <div ref="doughnutref">
                <Doughnut  title="Doughnut" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/> 
            </div>
            
        </div>
        <div class="box">
            <DownloadChart :chartRef="piechartref" filename="piechart_graph.png"/> 
            <div ref="piechartref">
                <PieChart title="PieChart" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/>
            </div>
            
        </div>
        <div class="box">Chart 4</div>
        <div class="box">Chart 5</div>
        <div class="box">Chart 6</div>
    </div>
  </div>
</template>

<script>
import FileUpload from './FileUpload.vue';
import Doughnut from './DoughnutGraph.vue';
import BarGraph from './BarGraph.vue';
import { ref } from 'vue';
import PieChart from './PieChart.vue';
import DownloadChart from './DownloadChart.vue';

export default {
  name: 'LandingPage',
  components: {
    BarGraph,
    Doughnut,
    FileUpload,
    PieChart,
    DownloadChart,
  },
  setup() {
    const bargraphref = ref(null);
    const doughnutref = ref(null);
    const piechartref = ref(null);
    const graphData = ref([]);

    const datainJSON = (data) => {
        graphData.value = data;
    };
    
    return {
        datainJSON,
        graphData,
        bargraphref,
        doughnutref,
        piechartref,
    };
  }
};
</script>

<style scoped>
.gridforGraph {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 1rem;
  margin-top: 2rem;
}

.box {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>