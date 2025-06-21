<template>
  <div class="graphs-container">
    <div v-if="graphsData.length" class="graphs-grid">
      <div 
        v-for="(graph, index) in graphsData" 
        :key="`graph-${index}`"
        class="graph-card"
      >
        <!-- Card Header -->
        <div class="card-header">
          <div class="card-info">
            <div class="graph-icon">
              <BarChart3 :size="24" />
            </div>
            <div class="graph-details">
              <h3 class="graph-name">{{ getGraphTitle(graph.graph_name) }}</h3>
              <div class="graph-id">
                <Hash :size="14" />
                {{ graph.graph_id }}
              </div>
            </div>
          </div>
          <button 
            @click="confirmDelete(graph.graph_id, index)"
            class="delete-button"
            :disabled="deletingGraphId === graph.graph_id"
            title="Delete Graph"
          >
            <Trash2 
              :size="16" 
              :class="{ 'animate-spin': deletingGraphId === graph.graph_id }"
            />
          </button>
        </div>

        <!-- Graph Content -->
        <div class="graph-content">
          <component
            :is="getGraphComponent(graph.graph_name)"
            :title="getGraphTitle(graph.graph_name)"
            :chartInput="graph.graph_data"
            v-if="isValidGraphType(graph.graph_name)"
          />
          
          <!-- Fallback for unknown graph types -->
          <div v-else class="unknown-graph">
            <AlertCircle :size="32" class="unknown-icon" />
            <p class="unknown-text">Unknown Graph Type: {{ graph.graph_name }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="loading" class="loading-state">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p class="loading-text">Loading your graphs...</p>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-content">
        <BarChart3 :size="64" class="empty-icon" />
        <h3 class="empty-title">No graphs yet</h3>
        <p class="empty-subtitle">Create your first graph to get started with data visualization</p>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
      <div class="modal-card" @click.stop>
        <div class="modal-header">
          <div class="modal-icon">
            <AlertTriangle :size="24" />
          </div>
          <div>
            <h3 class="modal-title">Delete Graph</h3>
            <p class="modal-subtitle">This action cannot be undone</p>
          </div>
        </div>
        
        <p class="modal-message">
          Are you sure you want to permanently delete this graph? All associated data will be lost.
        </p>
        
        <div class="modal-actions">
          <button @click="cancelDelete" class="btn-secondary">Cancel</button>
          <button @click="deleteGraph" class="btn-danger" :disabled="isDeleting">
            <Trash2 v-if="!isDeleting" :size="16" />
            <div v-else class="loading-spinner small"></div>
            {{ isDeleting ? 'Deleting...' : 'Delete Graph' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Trash2, AlertCircle, BarChart3, AlertTriangle, Hash } from 'lucide-vue-next'
import BarGraph from '@/components/BarGraph.vue'
import PIEChart from '@/components/PieChart.vue'
import DoughnutChart from '@/components/DoughnutGraph.vue'

export default {
  name: 'YourGraph',
  components: {
    BarGraph,
    PIEChart,
    DoughnutChart,
    Trash2,
    AlertCircle,
    BarChart3,
    AlertTriangle,
    Hash,
  },
  setup() {
    const graphsData = ref([])
    const loading = ref(true)
    const showDeleteModal = ref(false)
    const graphToDelete = ref(null)
    const indexToDelete = ref(null)
    const isDeleting = ref(false)
    const deletingGraphId = ref(null)

    // GRAPH CONFIGURATION
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
        component: 'DoughnutChart',
        title: 'Doughnut Chart'
      },
    }

    // Computed properties
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
          params: {
            graph_id: graphToDelete.value
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
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

    // API call
    onMounted(async () => {
      try {
        const token = sessionStorage.getItem('authToken')
        const response = await axios.get('http://localhost:8000/graph/mygraphs', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (response.data.data && Array.isArray(response.data.data)) {
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
      showDeleteModal,
      isDeleting,
      deletingGraphId,
      confirmDelete,
      cancelDelete,
      deleteGraph,
    }
  },
}
</script>

<style scoped>
.graphs-container {
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0 0;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
}

.graphs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .graphs-grid {
    grid-template-columns: 1fr;
  }
}

.graph-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.graph-card:hover {
  border-color: #c084fc;
  box-shadow: 0 4px 12px rgba(192, 132, 252, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.card-info {
  display: flex;
  gap: 12px;
  flex: 1;
}

.graph-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  color: white;
  padding: 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.graph-details {
  flex: 1;
}

.graph-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.graph-id {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.875rem;
  color: #64748b;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}

.delete-button {
  background: none;
  border: none;
  color: #ef4444;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-button:hover:not(:disabled) {
  background: #fee2e2;
  color: #dc2626;
}

.delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.graph-content {
  flex: 1;
  padding: 4px;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  border-radius: 12px;
  min-height: 300px;
  align-items: center;
  justify-content: center;
}

.unknown-graph {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #64748b;
}

.unknown-icon {
  color: #f59e0b;
}

.unknown-text {
  font-size: 0.875rem;
  margin: 0;
}

.loading-state,
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.loading-content,
.empty-content {
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

.loading-spinner.small {
  width: 16px;
  height: 16px;
  border-width: 2px;
}

.loading-text {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #475569;
  margin: 0 0 8px 0;
}

.empty-subtitle {
  color: #64748b;
  margin: 0;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.modal-icon {
  background: #fef3c7;
  color: #d97706;
  padding: 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.modal-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.modal-message {
  color: #475569;
  margin-bottom: 24px;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary,
.btn-danger {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-1px);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>