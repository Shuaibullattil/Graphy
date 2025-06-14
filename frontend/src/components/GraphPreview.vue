<template>
  <div class="bg-gray-50 p-4 rounded-lg">
    <div class="bg-white rounded p-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-violet-600 mx-auto mb-2"></div>
        <p class="text-gray-600">Loading preview...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-4xl mb-2">⚠️</div>
        <p class="text-red-600 mb-2">Failed to load preview</p>
        <p class="text-sm text-gray-500">{{ error }}</p>
        <button 
          @click="fetchPreview"
          class="mt-2 px-3 py-1 bg-violet-600 text-white text-sm rounded hover:bg-violet-700"
        >
          Retry
        </button>
      </div>

      <!-- Success State with Graph -->
      <div v-else-if="previewData && previewData.graph_data" class="text-center">
        <!-- Graph Component -->
        <div class="mb-4">
          <component 
            :is="getGraphComponent()"
            :title="previewData.name"
            :chartInput="previewData.graph_data"
            v-if="getGraphComponent()"
          />
        </div>
        
        <!-- Graph Info -->
        <div class="border-t pt-4">
          <p class="font-medium text-gray-800">{{ previewData.name }}</p>
          <p class="text-sm text-gray-600">Type: {{ getGraphTitle() }}</p>
          <p class="text-xs text-gray-400 mt-1">
            Labels: {{ previewData.labels.join(', ') }}
          </p>
          <p class="text-xs text-gray-400">
            Data Points: {{ previewData.graph_data.length }}
          </p>
        </div>
      </div>

      <!-- Default/Empty State -->
      <div v-else class="text-center py-8">
        <div class="text-4xl mb-2">📊</div>
        <p class="text-gray-600">{{ previewProps.name || 'Graph Preview' }}</p>
        <p class="text-sm text-gray-500">Select options to see preview</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'
import axios from 'axios'
import BarGraph from './BarGraph.vue'
import PIEChart from './PieChart.vue'
import DoughnutGraph from './DoughnutGraph.vue'

export default {
  name: 'GraphPreview',
  components: {
    BarGraph,
    PIEChart,
    DoughnutGraph
  },
  props: {
    previewProps: {
      type: Object,
      required: true,
      validator(value) {
        return value && 
               typeof value.name === 'string' &&
               typeof value.file_id === 'string' &&
               typeof value.sheetName === 'string' &&
               Array.isArray(value.labels) &&
               typeof value.graph_id === 'string'
      }
    }
  },
  setup(props) {
    const loading = ref(false)
    const error = ref(null)
    const previewData = ref(null)

    const graphConfig = {
      '001': {
        component: 'BarGraph',
        title: 'Bar Chart'
      },
      '002': {
        component: 'PIEChart',
        title: 'Pie Chart'
      },
      '003': {
        component: 'DoughnutGraph',
        title: 'Doughnut Chart'
      }
    }

    const isValidForPreview = computed(() => {
      return props.previewProps.name.trim() !== '' &&
             props.previewProps.labels.length > 0 &&
             props.previewProps.graph_id !== '' &&
             props.previewProps.file_id !== ''
    })

    const getGraphComponent = () => {
      const config = graphConfig[props.previewProps.graph_id]
      return config ? config.component : null
    }

    const getGraphTitle = () => {
      const config = graphConfig[props.previewProps.graph_id]
      return config ? config.title : 'Unknown'
    }

    const fetchPreview = async () => {
      if (!isValidForPreview.value) {
        previewData.value = null
        return
      }

      loading.value = true
      error.value = null

      try {
        const token = sessionStorage.getItem('authToken')
        
        // Check if token exists
        if (!token) {
          throw new Error('No authentication token found')
        }

        // Create query parameters
        const params = new URLSearchParams({
          name: props.previewProps.name,
          file_id: props.previewProps.file_id,
          sheetName: props.previewProps.sheetName,
          labels: props.previewProps.labels.join(','), // Convert array to comma-separated string
          graph_id: props.previewProps.graph_id
        })

        const response = await axios.get(
          `http://localhost:8000/graph/my-graph-preview?${params}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        )

        previewData.value = response.data
      } catch (err) {
        console.error('Error fetching preview:', err)
        if (err.response?.status === 401) {
          error.value = 'Authentication failed. Please login again.'
        } else {
          error.value = err.response?.data?.detail || err.message || 'Failed to load preview'
        }
        previewData.value = null
      } finally {
        loading.value = false
      }
    }

    // Watch for changes in preview props and refetch
    watch(
      () => props.previewProps,
      () => {
        fetchPreview()
      },
      { deep: true, immediate: true }
    )

    return {
      loading,
      error,
      previewData,
      fetchPreview,
      getGraphComponent,
      getGraphTitle
    }
  }
}
</script>