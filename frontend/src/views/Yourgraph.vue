<!-- Main Component: YourGraph.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
    <!-- Header with Create Dashboard Button -->
    <div class="max-w-7xl mx-auto mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-slate-800 mb-2">My Graphs</h1>
          <p class="text-slate-600">Manage and organize your data visualizations</p>
        </div>
        <button
          @click="toggleDashboardCreation"
          class="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-xl 
                 font-medium hover:from-purple-600 hover:to-purple-700 transition-all duration-200 
                 shadow-lg hover:shadow-xl flex items-center gap-2"
        >
          <Plus class="h-5 w-5" />
          {{ isDashboardMode ? 'Exit Dashboard Mode' : 'Create Dashboard' }}
        </button>
      </div>
    </div>

    <!-- Dashboard Creation Mode -->
    <DashboardCreator
      v-if="isDashboardMode"
      :graphs-data="graphsData"
      :available-graph-types="availableGraphTypes"
      :get-graph-title="getGraphTitle"
      :get-graph-component="getGraphComponent"
      :is-valid-graph-type="isValidGraphType"
      @close="toggleDashboardCreation"
      @dashboard-created="onDashboardCreated"
    />

    <!-- Normal Graph View -->
    <div v-else>
      <!-- Enhanced Search and Filter Bar -->
      <SearchFilterBar
        v-model:search-query="searchQuery"
        v-model:selected-type="selectedType"
        v-model:file-name="fileName"
        :file-names="fileNames"
        :available-graph-types="availableGraphTypes"
        :filtered-count="filteredCount"
        :get-graph-title="getGraphTitle"
        @search="handleSearch"
      />

      <!-- Graphs Grid -->
      <div class="max-w-7xl mx-auto">
        <GraphGrid
          :graphs="graphsData"
          :loading="loading"
          :deleting-graph-id="deletingGraphId"
          :get-graph-title="getGraphTitle"
          :get-graph-component="getGraphComponent"
          :is-valid-graph-type="isValidGraphType"
          @confirm-delete="confirmDelete"
        />
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <DeleteModal
      :show="showDeleteModal"
      :is-deleting="isDeleting"
      @confirm="deleteGraph"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Plus } from 'lucide-vue-next'
import SearchFilterBar from '../components/SearchFilterBar.vue'
import GraphGrid from '../components/GraphGrid.vue'
import DeleteModal from '../components/DeleteModal.vue'
import DashboardCreator from '../components/DashboardCreator.vue'
import BarGraph from '@/components/BarGraph.vue'
import PIEChart from '@/components/PieChart.vue'
import DoughnutChart from '@/components/DoughnutGraph.vue'
import { api } from '../services/api.js'

export default {
  name: 'YourGraph',
  components: {
    SearchFilterBar,
    GraphGrid,
    DeleteModal,
    DashboardCreator,
    Plus,
  },
  setup() {
    const graphsData = ref([])
    const loading = ref(true)
    const showDeleteModal = ref(false)
    const graphToDelete = ref(null)
    const indexToDelete = ref(null)
    const isDeleting = ref(false)
    const deletingGraphId = ref(null)
    const isDashboardMode = ref(false)
    const fileNames = ref([])
    const fileName = ref('')
    const searchQuery = ref('')
    const selectedType = ref('')
    const filteredCount = ref(0)

    // GRAPH CONFIGURATION
    const graphConfig = {
      '001': { component: 'BarGraph', title: 'Bar Chart' },
      '002': { component: 'PIEChart', title: 'Pie Chart' },
      '003': { component: 'DoughnutChart', title: 'Doughnut Chart' },
    }

    // Computed properties
    const availableGraphTypes = computed(() => Object.keys(graphConfig))

    // Helper functions
    const isValidGraphType = (graphName) => graphName in graphConfig
    const getGraphComponent = (graphName) => graphConfig[graphName]?.component || 'div'
    const getGraphTitle = (graphName) => graphConfig[graphName]?.title || `Graph ${graphName}`

    // Dashboard functions
    const toggleDashboardCreation = () => {
      isDashboardMode.value = !isDashboardMode.value
    }

    const onDashboardCreated = () => {
      isDashboardMode.value = false
      // Optionally refresh graphs or show success message
    }

    // Delete functions
    const confirmDelete = (graphId, index) => {
      graphToDelete.value = graphId
      indexToDelete.value = index
      showDeleteModal.value = true
    }

    const cancelDelete = () => {
      showDeleteModal.value = false
      graphToDelete.value = null
      indexToDelete.value = null
    }

    const deleteGraph = async () => {
      if (!graphToDelete.value) return

      isDeleting.value = true
      deletingGraphId.value = graphToDelete.value

      try {
        const token = sessionStorage.getItem('authToken')
        const baseUrl = 'http://localhost:8000'
        
        await axios.delete(`${baseUrl}/graph/drop`, {
          params: { graph_id: graphToDelete.value },
          headers: { Authorization: `Bearer ${token}` },
        })

        graphsData.value.splice(indexToDelete.value, 1)
        console.log('Graph deleted successfully')
        
      } catch (error) {
        console.error('Error deleting graph:', error)
        alert('Failed to delete graph. Please try again.')
      } finally {
        isDeleting.value = false
        deletingGraphId.value = null
        showDeleteModal.value = false
        graphToDelete.value = null
        indexToDelete.value = null
      }
    }

    // Fetch all file names
    const fetchFileNames = async () => {
      try {
        const res = await api.getAllFileNames()
        fileNames.value = res.files || []
      } catch (e) {
        fileNames.value = []
      }
    }

    // Fetch all graphs (default)
    const fetchAllGraphs = async () => {
      loading.value = true
      try {
        const res = await api.getAllMyGraphs()
        graphsData.value = res.data || []
        filteredCount.value = (res.data || []).length
      } catch (e) {
        graphsData.value = []
        filteredCount.value = 0
      } finally {
        loading.value = false
      }
    }

    // Search graphs
    const searchGraphs = async () => {
      loading.value = true
      try {
        // Only search if any filter is set
        if (searchQuery.value || selectedType.value || fileName.value) {
          const res = await api.searchGraphs({
            name: searchQuery.value,
            graph_type: selectedType.value,
            filename: fileName.value,
          })
          graphsData.value = res.data || []
          filteredCount.value = res.count || 0
        } else {
          await fetchAllGraphs()
        }
      } catch (e) {
        graphsData.value = []
        filteredCount.value = 0
      } finally {
        loading.value = false
      }
    }

    // Handler for SearchFilterBar
    const handleSearch = ({ searchQuery: sq, selectedType: st, fileName: fn }) => {
      searchQuery.value = sq
      selectedType.value = st
      fileName.value = fn
      searchGraphs()
    }

    onMounted(async () => {
      await fetchFileNames()
      await fetchAllGraphs()
    })

    return {
      graphsData,
      loading,
      availableGraphTypes,
      isValidGraphType,
      getGraphComponent,
      getGraphTitle,
      showDeleteModal,
      isDeleting,
      deletingGraphId,
      confirmDelete,
      cancelDelete,
      deleteGraph,
      searchQuery,
      selectedType,
      filteredCount,
      fileNames,
      fileName,
      handleSearch,
      isDashboardMode,
      toggleDashboardCreation,
      onDashboardCreated,
    }
  },
}
</script>