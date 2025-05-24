<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-royal-purple to-purple-900 text-white overflow-hidden">
    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-royal-purple bg-opacity-30 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-lilac bg-opacity-20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div class="absolute top-1/2 left-1/4 w-64 h-64 bg-fairy-tale bg-opacity-15 rounded-full blur-2xl float-animation"></div>
      <div class="absolute top-1/3 right-1/3 w-72 h-72 bg-purple-600 bg-opacity-25 rounded-full blur-3xl float-animation" style="animation-delay: 2s;"></div>
    </div>

    <!-- Navigation -->
    <nav class="relative z-10 flex justify-between items-center p-6 lg:px-12">
      <div class="flex items-center space-x-2">
        <TrendingUp class="w-8 h-8 text-white" />
        <span class="text-2xl font-bold">GRAPHY</span>
      </div>
      <button 
        @click="navigateToDashboard"
        class="hidden md:flex items-center space-x-2 bg-royal-purple bg-opacity-40 backdrop-blur-sm px-6 py-2 rounded-full hover:bg-opacity-60 border border-lilac border-opacity-30 transition-all duration-300 group"
      >
        <span>Dashboard</span>
        <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
      </button>
    </nav>

    <!-- Hero Section -->
    <section class="relative z-10 text-center px-6 lg:px-12 pt-12 pb-20">
      <div 
        class="transform transition-all duration-1000"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
      >
        <div class="inline-flex items-center space-x-2 bg-gray-800 bg-opacity-60 backdrop-blur-sm px-4 py-2 rounded-full mb-6 border border-royal-purple border-opacity-40">
          <Star class="w-4 h-4 text-yellow-300" />
          <span class="text-sm font-medium">Lightweight & Powerful Data Visualization</span>
        </div>
        
        <h1 class="text-5xl lg:text-7xl font-bold mb-6 leading-tight">
          Turn Your Excel into
          <br />
          <span class="gradient-text">Beautiful Charts</span>
        </h1>
        
        <p class="text-xl lg:text-2xl mb-8 max-w-3xl mx-auto leading-relaxed opacity-90">
          A lightweight, powerful tool to visualize Excel data and monitor team or personal performance in real time.
          <br />
          <span class="text-fairy-tale">Simple. Fast. Elegant.</span>
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button 
            @click="navigateToDashboard"
            class="group bg-gradient-to-r from-royal-purple to-lilac text-white px-8 py-4 rounded-full font-bold text-lg hover:from-purple-700 hover:to-fairy-tale transition-all duration-300 transform hover:scale-105 shadow-2xl flex items-center space-x-2 border border-lilac border-opacity-40"
          >
            <Play class="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            <span>START VISUALIZING</span>
          </button>
          
          <div class="flex items-center space-x-2 text-fairy-tale">
            <CheckCircle class="w-5 h-5" />
            <span>Free to get started</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Chart Demo -->
    <section class="relative z-10 px-6 lg:px-12 pb-20">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold mb-4">See It In Action</h2>
          <p class="text-xl opacity-90">Watch your data transform into beautiful visualizations</p>
        </div>
        
        <div class="grid lg:grid-cols-3 gap-8">
          <div 
            v-for="(chart, index) in chartTypes" 
            :key="index"
            class="bg-gray-800 bg-opacity-60 backdrop-blur-sm rounded-2xl p-6 transition-all duration-500 transform hover:scale-105 cursor-pointer border border-royal-purple border-opacity-30 hover:border-opacity-60"
            :class="currentChart === index ? 'ring-2 ring-lilac ring-opacity-70 bg-opacity-80 border-lilac' : ''"
            @click="currentChart = index"
          >
            <div class="h-48 bg-gray-900 bg-opacity-40 rounded-xl mb-4 flex items-center justify-center relative overflow-hidden border border-gray-700">
              <div 
                class="absolute inset-0 opacity-20" 
                :style="{ background: `linear-gradient(135deg, ${chart.color} 0%, ${chart.secondaryColor} 100%)` }"
              ></div>
              <div 
                class="w-24 h-24 rounded-full flex items-center justify-center text-white font-bold text-lg relative z-10 transform transition-all duration-300 hover:scale-110"
                :style="{ backgroundColor: chart.color }"
              >
                <component :is="chart.icon" class="w-10 h-10" />
              </div>
            </div>
            <h3 class="text-xl font-semibold text-center">{{ chart.name }}</h3>
            <p class="text-sm opacity-75 text-center mt-2">{{ chart.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="relative z-10 px-6 lg:px-12 py-20 bg-gray-900 bg-opacity-60 backdrop-blur-sm border-y border-gray-700 border-opacity-50">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-bold mb-6">Powerful Features</h2>
          <p class="text-xl opacity-90 max-w-2xl mx-auto">
            Everything you need to transform your data into actionable insights
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="bg-gray-800 bg-opacity-60 backdrop-blur-sm rounded-2xl p-8 hover:bg-opacity-80 transition-all duration-300 transform hover:-translate-y-2 group border border-royal-purple border-opacity-30 hover:border-opacity-60"
          >
            <div class="text-fairy-tale mb-4 group-hover:scale-110 transition-transform duration-300">
              <component :is="feature.icon" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
            <p class="opacity-90 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="relative z-10 px-6 lg:px-12 py-20">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-bold mb-12">Trusted by Teams Worldwide</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-gray-800 bg-opacity-60 backdrop-blur-sm rounded-xl p-6 border border-royal-purple border-opacity-30">
            <div class="text-4xl font-bold mb-2 text-lilac">10k+</div>
            <div class="opacity-90">Charts Created</div>
          </div>
          <div class="bg-gray-800 bg-opacity-60 backdrop-blur-sm rounded-xl p-6 border border-royal-purple border-opacity-30">
            <div class="text-4xl font-bold mb-2 text-lilac">500+</div>
            <div class="opacity-90">Organizations</div>
          </div>
          <div class="bg-gray-800 bg-opacity-60 backdrop-blur-sm rounded-xl p-6 border border-royal-purple border-opacity-30">
            <div class="text-4xl font-bold mb-2 text-lilac">99.9%</div>
            <div class="opacity-90">Uptime</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="relative z-10 text-center px-6 lg:px-12 py-20">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl lg:text-5xl font-bold mb-6">
          Ready to Visualize Your Data?
        </h2>
        <p class="text-xl mb-8 opacity-90">
          Join thousands of users who have transformed their Excel files into beautiful, actionable dashboards.
        </p>
        
        <button 
          @click="navigateToDashboard"
          class="group bg-gradient-to-r from-royal-purple to-lilac text-white px-12 py-4 rounded-full font-bold text-xl hover:from-purple-800 hover:to-fairy-tale transition-all duration-300 transform hover:scale-105 shadow-2xl inline-flex items-center space-x-3 border border-lilac border-opacity-50"
        >
          <span>GET STARTED NOW</span>
          <ArrowRight class="w-6 h-6 group-hover:translate-x-2 transition-transform duration-300" />
        </button>
        
        <div class="flex justify-center items-center space-x-8 mt-8 text-fairy-tale flex-wrap gap-4">
          <div class="flex items-center space-x-2">
            <CheckCircle class="w-5 h-5" />
            <span>No credit card required</span>
          </div>
          <div class="flex items-center space-x-2">
            <CheckCircle class="w-5 h-5" />
            <span>Start in minutes</span>
          </div>
          <div class="flex items-center space-x-2">
            <ShieldCheck class="w-5 h-5" />
            <span>Secure & Private</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="relative z-10 text-center py-8 border-t border-gray-700 border-opacity-50 bg-gray-900 bg-opacity-60">
      <div class="flex items-center justify-center space-x-2 mb-4">
        <TrendingUp class="w-6 h-6" />
        <span class="text-xl font-bold">GRAPHY</span>
      </div>
      <p class="opacity-70">© 2025 GRAPHY. Making data visualization simple and beautiful.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  TrendingUp, 
  ArrowRight, 
  Star, 
  Play, 
  CheckCircle, 
  Upload, 
  BarChart3, 
  Users, 
  PieChart, 
  Eye, 
  Zap,
  ShieldCheck
} from 'lucide-vue-next'

// Router setup
const router = useRouter()

// Reactive data
const isVisible = ref(false)
const currentChart = ref(0)

// Navigation function
const navigateToDashboard = () => {
  router.push('/dashboard')
}

// Features data
const features = ref([
  {
    icon: Upload,
    title: "Upload Excel Files",
    description: "Convert your Excel data into stunning charts and graphs with just a few clicks"
  },
  {
    icon: BarChart3,
    title: "Multiple Dashboard System", 
    description: "Create separate dashboards for startup, personal projects, and company work"
  },
  {
    icon: Users,
    title: "Organization Spaces",
    description: "Create or join organizations and share files with team members seamlessly"
  },
  {
    icon: PieChart,
    title: "Flexible Graph Options",
    description: "Choose from bar, pie, line, doughnut charts and more visualization types"
  },
  {
    icon: Eye,
    title: "Real-time Monitoring",
    description: "Track team and personal performance with live, customizable dashboards"
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Instant visualization of your data with our optimized rendering engine"
  }
])

// Chart types data
const chartTypes = ref([
  { 
    name: "Bar Chart", 
    color: "#7E52A0", 
    secondaryColor: "#9333ea",
    icon: BarChart3,
    description: "Perfect for comparing categories"
  },
  { 
    name: "Pie Chart", 
    color: "#D295BF", 
    secondaryColor: "#ec4899",
    icon: PieChart,
    description: "Show proportions and percentages"
  },
  { 
    name: "Line Chart", 
    color: "#E6BCCD", 
    secondaryColor: "#f472b6",
    icon: TrendingUp,
    description: "Track trends over time"
  }
])

// Lifecycle hooks
onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)

  // Auto-rotate charts
  setInterval(() => {
    currentChart.value = (currentChart.value + 1) % chartTypes.value.length
  }, 4000)
})
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.float-animation { 
  animation: float 6s ease-in-out infinite; 
}

.gradient-text {
  background: linear-gradient(135deg, #E6BCCD 0%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.delay-1000 {
  animation-delay: 1s;
}
</style>