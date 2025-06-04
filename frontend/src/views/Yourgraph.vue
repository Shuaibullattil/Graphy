<template>
  <div class="graphs-container">
    <div v-if="graphsData.length" class="graphs-grid">
      <div 
        v-for="(graph, index) in graphsData" 
        :key="`graph-${index}`"
        class="graph-item"
      >
        <!-- Dynamic Component Rendering -->
        <component
          :is="getGraphComponent(graph.graph_name)"
          :title="getGraphTitle(graph.graph_name)"
          :chartInput="graph.graph_data"
          v-if="isValidGraphType(graph.graph_name)"
        />
        
        <!-- Fallback for unknown graph types -->
        <div v-else class="unknown-graph">
          <h3>Unknown Graph Type</h3>
          <p>Graph name: {{ graph.graph_name }}</p>
          <p>Available types: {{ availableGraphTypes.join(', ') }}</p>
        </div>
      </div>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <p>Loading chart data...</p>
    </div>
    
    <div v-else class="no-data-state">
      <p>No graph data available.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import BarGraph from '@/components/BarGraph.vue'
import PIEChart from '@/components/PieChart.vue'
import DoughnutChart from '@/components/DoughnutGraph.vue'
// Import new graph components here
// import LineChart from '@/components/LineChart.vue'
// import AreaChart from '@/components/AreaChart.vue'

export default {
  name: 'YourGraph',
  components: {
    BarGraph,
    PIEChart,
    DoughnutChart,
    // Register new components here
    // LineChart,
    // AreaChart,
  },
  setup() {
    const graphsData = ref([])
    const loading = ref(true)

    // GRAPH CONFIGURATION - Easy to extend!
    const graphConfig = {
      '001': {
        component: 'BarGraph',
        title: 'Sales by Month'
      },
      '002': {
        component: 'PIEChart',
        title: 'Sales Distribution'
      },
      '003': {
        component: 'DoughnutChart',
        title: 'Sales Analysis'
      },
      // Add new graph types here:
      // '004': {
      //   component: 'LineChart',
      //   title: 'Sales Trend'
      // },
      // '005': {
      //   component: 'AreaChart',
      //   title: 'Sales Area Analysis'
      // },
    }

    // Computed properties for easy access
    const availableGraphTypes = computed(() => Object.keys(graphConfig))

    // Helper functions
    const isValidGraphType = (graphName) => {
      return graphName in graphConfig
    }

    const getGraphComponent = (graphName) => {
      return graphConfig[graphName]?.component || 'div'
    }

    const getGraphTitle = (graphName) => {
      return graphConfig[graphName]?.title || `Graph ${graphName}`
    }

    // API call
    onMounted(async () => {
      try {
        const token = sessionStorage.getItem('authToken')
        const response = await axios.get('http://localhost:8000/graph/mygraphs', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        // Check if response has data array
        if (response.data.data && Array.isArray(response.data.data)) {
          // Filter graphs that have valid graph_data
          graphsData.value = response.data.data.filter(graph => 
            graph.graph_data && Array.isArray(graph.graph_data) && graph.graph_data.length > 0
          )
        }

      } catch (error) {
        console.error('Error fetching graph data:', error)
      } finally {
        loading.value = false
      }
    })

    return {
      graphsData,
      loading,
      availableGraphTypes,
      isValidGraphType,
      getGraphComponent,
      getGraphTitle,
    }
  },
}
</script>

<style scoped>
.graphs-container {
  padding: 20px;
}

.graphs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* For larger screens, ensure exactly 3 columns */
@media (min-width: 1200px) {
  .graphs-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* For medium screens, 2 columns */
@media (min-width: 768px) and (max-width: 1199px) {
  .graphs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* For small screens, 1 column */
@media (max-width: 767px) {
  .graphs-grid {
    grid-template-columns: 1fr;
  }
  
  .graph-item {
    min-width: 300px;
  }
}

.graph-item {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.loading-state,
.no-data-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  font-size: 18px;
  color: #666;
}

.unknown-graph {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #666;
  text-align: center;
}

.unknown-graph h3 {
  margin-bottom: 8px;
  color: #333;
}

.unknown-graph p {
  margin: 4px 0;
  font-size: 14px;
}
</style>