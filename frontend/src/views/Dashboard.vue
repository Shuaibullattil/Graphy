<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Sidebar Component -->
    <Sidebar v-model="activeTab" @tab-changed="handleTabChange" />
    
    <!-- Main Content Area -->
    <div class="lg:ml-64 min-h-screen">
      <!-- Header -->
      <header class="bg-white/80 backdrop-blur-lg shadow-sm border-b border-gray-200/50 px-4 sm:px-6 lg:px-8 py-6 sticky top-0 z-20">
        <div class="flex items-center justify-between">
          <div class="ml-12 lg:ml-0">
            <h1 class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-purple-400 bg-clip-text text-transparent">
              {{ getPageTitle() }}
            </h1>
            <p class="text-gray-600 mt-1 text-sm sm:text-base">{{ getPageDescription() }}</p>
          </div>
          
          <!-- Status Indicator -->
          <div v-if="graphData.length > 0" class="hidden sm:flex items-center space-x-3 px-4 py-2 rounded-full bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium text-green-700">Data loaded successfully</span>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="p-2 sm:p-2 lg:p-2">
        <!-- Dashboard Content -->
        <div v-if="activeTab === 'Dashboard'" class="space-y-6 sm:space-y-8">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 text-center">
              <mydashboards />
          </div>
          
        </div>

        <!-- Other Tab Contents -->
        <div v-else-if="activeTab === 'Your Files'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 text-center">
            <myfiles />
          </div>
        </div>

        <div v-else-if="activeTab === 'Table'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <Yourtable />
          </div>
        </div>

        <div v-else-if="activeTab === 'Graphs'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <Yourgraph />
          </div>
        </div>

        <div v-else-if="activeTab === 'Account'" class="space-y-6">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center">
            <div class="w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center" style="background: linear-gradient(135deg, #d295bf 0%, #e6bccd 100%)">
              <User class="w-10 h-10 text-white" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Account Settings</h3>
            <p class="text-gray-600 mb-6">Manage your profile and preferences</p>
            <div class="inline-flex items-center px-6 py-3 rounded-xl text-white font-medium" style="background: linear-gradient(135deg, #e6bccd 0%, #7e52a0 100%)">
              <Clock class="w-4 h-4 mr-2" />
              Coming Soon
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import FileUpload from '@/components/FileUpload.vue';
import Doughnut from '@/components/DoughnutGraph.vue';
import BarGraph from '@/components/BarGraph.vue';
import PIEChart from '@/components/PieChart.vue';
import DownloadChart from '@/components/DownloadChart.vue';
import Yourtable from '@/views/Table.vue'
import Yourgraph from './Yourgraph.vue';
import Myfiles from './Myfiles.vue';
import Mydashboards from './Mydashboards.vue';
import { ref } from 'vue';
import { 
  Upload,
  PieChart as PieChartIcon,
  TrendingUp,
  Activity,
  BarChart,
  BarChart3,
  FileText,
  User,
  Clock
} from 'lucide-vue-next';

export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    FileUpload,
    Doughnut,
    BarGraph,
    PIEChart,
    DownloadChart,
    Upload,
    PieChart: PieChartIcon,
    TrendingUp,
    Activity,
    BarChart,
    BarChart3,
    FileText,
    User,
    Clock,
    Yourtable,
    Yourgraph,
    Myfiles,
    Mydashboards
  },
  setup() {
    const bargraphref = ref(null);
    const doughnutref = ref(null);
    const piechartref = ref(null);
    const graphData = ref([]);
    const activeTab = ref('Dashboard');

    const datainJSON = (data) => {
      graphData.value = data;
    };

    const handleTabChange = (tabName) => {
      activeTab.value = tabName;
    };

    const getPageTitle = () => {
      const titles = {
        'Dashboard': 'Data Visualization Dashboard',
        'Your Files': 'Your Files',
        'Graphs': 'Graph Library',
        'Table': 'Data Tables',
        'Account': 'Account Settings'
      };
      return titles[activeTab.value] || 'Dashboard';
    };

    const getPageDescription = () => {
      const descriptions = {
        'Dashboard': 'Create and manage your data visualizations with style',
        'Your Files': 'Manage your uploaded files and data sources',
        'Graphs': 'Explore different chart types and visualization options',
        'Table': 'Edit Your data table here',
        'Account': 'Manage your account settings and preferences'
      };
      return descriptions[activeTab.value] || '';
    };

    const getCurrentTime = () => {
      const now = new Date();
      return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      });
    };
    
    return {
      datainJSON,
      graphData,
      bargraphref,
      doughnutref,
      piechartref,
      activeTab,
      handleTabChange,
      getPageTitle,
      getPageDescription,
      getCurrentTime
    };
  }
};
</script>