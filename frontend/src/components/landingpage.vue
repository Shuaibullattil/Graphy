<template>
  <div>
    <h1>Landing Page</h1>
    <button @click="$router.push('/pageone')">Go to Page One</button>
    <button @click="$router.push('/pagetwo')">Go to Page Two</button>
    <button @click="$router.push('/pagethree')">Go to Page Three</button>
    <FileUpload @dataParsed="datainJSON"/>
    <p>{{graphData}}</p>
    <div class="gridforGraph">
        <div class="box"><BarGraph title="Bargraph" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/></div>
        <div class="box"> <Doughnut title="Doughnut" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/> </div>
        <div class="box"><BarGraph title="Bargraph" :jsonUrl="graphData.length > 0 ? graphData : '/sampledata.json'"/></div>
        <div class="box">Chart 4</div>
        <div class="box">Chart 5</div>
        <div class="box">Chart 6</div>
    </div>

  </div>
</template>

<script >
import FileUpload from './FileUpload.vue';
import Doughnut from './DoughnutGraph.vue';
import BarGraph from './BarGraph.vue';
import { ref } from 'vue';
export default {
  name: 'LandingPage',
  components: {
    BarGraph,
    Doughnut,
    FileUpload,
  },
  setup(){
    const graphData = ref([])

    const datainJSON = (data) =>{
        graphData.value = data
    }
    return{
        datainJSON,
        graphData,
    }
  }
}
 

</script>
