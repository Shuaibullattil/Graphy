<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
    <!-- Background Effects -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-2s"></div>
      <div class="absolute top-40 left-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-4s"></div>
    </div>

    <!-- Main Container -->
    <div class="relative z-10 w-full max-w-md">
      <!-- Glass Card -->
      <div class="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <Lock class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-3xl font-bold text-white mb-2">
            {{ isLogin ? 'Welcome Back' : 'Create Account' }}
          </h1>
          <p class="text-gray-300">
            {{ isLogin ? 'Sign in to your account' : 'Join us today and get started' }}
          </p>
        </div>

        <!-- Form Toggle Buttons -->
        <div class="flex bg-white/5 rounded-2xl p-1 mb-8">
          <button
            @click="isLogin = true"
            :class="[
              'flex-1 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300',
              isLogin 
                ? 'bg-gradient-to-r from-purple-500 to-cyan-500 text-white shadow-lg' 
                : 'text-gray-300 hover:text-white'
            ]"
          >
            Sign In
          </button>
          <button
            @click="isLogin = false"
            :class="[
              'flex-1 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300',
              !isLogin 
                ? 'bg-gradient-to-r from-purple-500 to-cyan-500 text-white shadow-lg' 
                : 'text-gray-300 hover:text-white'
            ]"
          >
            Sign Up
          </button>
        </div>

        <!-- Login Form -->
        <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email Field -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Email</label>
            <div class="relative">
              <input
                v-model="loginForm.email"
                type="email"
                required
                class="w-full px-4 py-3 pl-12 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Enter your email"
              />
              <Mail class="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <!-- Password Field -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Password</label>
            <div class="relative">
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-4 py-3 pl-12 pr-12 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Enter your password"
              />
              <Lock class="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-3.5 w-5 h-5 text-gray-400 hover:text-white transition-colors"
              >
                <EyeOff v-if="showPassword" class="w-5 h-5" />
                <Eye v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input type="checkbox" v-model="rememberMe" class="w-4 h-4 text-purple-500 bg-white/5 border-white/10 rounded focus:ring-purple-500">
              <span class="ml-2 text-sm text-gray-300">Remember me</span>
            </label>
            <a href="#" class="text-sm text-purple-400 hover:text-purple-300 transition-colors">
              Forgot password?
            </a>
          </div>

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-cyan-500 text-white font-medium rounded-xl hover:from-purple-600 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <Loader2 v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
            <span v-if="isLoading">Signing in...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <!-- Registration Form -->
        <form v-else @submit.prevent="handleRegister" class="space-y-6">
          <!-- Name Field -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Full Name</label>
            <div class="relative">
              <input
                v-model="registerForm.name"
                type="text"
                required
                class="w-full px-4 py-3 pl-12 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Enter your full name"
              />
              <User class="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <!-- Email Field -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Email</label>
            <div class="relative">
              <input
                v-model="registerForm.email"
                type="email"
                required
                class="w-full px-4 py-3 pl-12 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Enter your email"
              />
              <Mail class="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <!-- Password Field -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Password</label>
            <div class="relative">
              <input
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-4 py-3 pl-12 pr-12 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
                placeholder="Create a password"
              />
              <Lock class="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-3.5 w-5 h-5 text-gray-400 hover:text-white transition-colors"
              >
                <EyeOff v-if="showPassword" class="w-5 h-5" />
                <Eye v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Account Type -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-300">Account Type</label>
            <div class="grid grid-cols-2 gap-4">
              <label class="cursor-pointer">
                <input
                  type="radio"
                  value="personal"
                  v-model="registerForm.accountType"
                  class="sr-only"
                />
                <div :class="[
                  'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:border-white/20',
                  registerForm.accountType === 'personal'
                    ? 'border-purple-500 bg-purple-500/20 text-white'
                    : 'border-white/10 bg-white/5 text-gray-300'
                ]">
                  <User class="w-6 h-6 mx-auto mb-2" />
                  <span class="text-sm font-medium">Personal</span>
                </div>
              </label>
              <label class="cursor-pointer">
                <input
                  type="radio"
                  value="team"
                  v-model="registerForm.accountType"
                  class="sr-only"
                />
                <div :class="[
                  'p-4 rounded-xl border-2 transition-all duration-300 text-center hover:border-white/20',
                  registerForm.accountType === 'team'
                    ? 'border-purple-500 bg-purple-500/20 text-white'
                    : 'border-white/10 bg-white/5 text-gray-300'
                ]">
                  <Users class="w-6 h-6 mx-auto mb-2" />
                  <span class="text-sm font-medium">Team</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Terms & Conditions -->
          <div class="flex items-start space-x-3">
            <input
              type="checkbox"
              v-model="acceptTerms"
              required
              class="w-4 h-4 mt-1 text-purple-500 bg-white/5 border-white/10 rounded focus:ring-purple-500"
            />
            <label class="text-sm text-gray-300">
              I agree to the <a href="#" class="text-purple-400 hover:text-purple-300 underline">Terms of Service</a> and <a href="#" class="text-purple-400 hover:text-purple-300 underline">Privacy Policy</a>
            </label>
          </div>

          <!-- Register Button -->
          <button
            type="submit"
            :disabled="isLoading || !acceptTerms"
            class="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-cyan-500 text-white font-medium rounded-xl hover:from-purple-600 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <Loader2 v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
            <span v-if="isLoading">Creating account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl flex items-center space-x-3">
          <AlertCircle class="w-5 h-5 text-red-400 flex-shrink-0" />
          <p class="text-red-400 text-sm">{{ errorMessage }}</p>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="mt-6 p-4 bg-green-500/20 border border-green-500/30 rounded-xl flex items-center space-x-3">
          <CheckCircle class="w-5 h-5 text-green-400 flex-shrink-0" />
          <p class="text-green-400 text-sm">{{ successMessage }}</p>
        </div>

        <!-- Social Login Options -->
        <div class="mt-8">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-white/10"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-slate-900 text-gray-400">Or continue with</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <button
              type="button"
              class="w-full inline-flex justify-center py-3 px-4 rounded-xl border border-white/10 bg-white/5 text-sm font-medium text-gray-300 hover:bg-white/10 transition-all duration-300"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span class="ml-2">Google</span>
            </button>

            <button
              type="button"
              class="w-full inline-flex justify-center py-3 px-4 rounded-xl border border-white/10 bg-white/5 text-sm font-medium text-gray-300 hover:bg-white/10 transition-all duration-300"
            >
              <Github class="w-5 h-5" />
              <span class="ml-2">GitHub</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { 
  Lock, 
  Mail, 
  Eye, 
  EyeOff, 
  User, 
  Users, 
  Loader2, 
  AlertCircle, 
  CheckCircle,
  Github
} from 'lucide-vue-next'
import { api } from '@/services/api'

export default {
  name: 'LoginRegisterPage',
  components: {
    Lock,
    Mail,
    Eye,
    EyeOff,
    User,
    Users,
    Loader2,
    AlertCircle,
    CheckCircle,
    Github
  },
  data() {
    return {
      isLogin: true,
      showPassword: false,
      isLoading: false,
      rememberMe: false,
      acceptTerms: false,
      errorMessage: '',
      successMessage: '',
      loginForm: {
        email: '',
        password: ''
      },
      registerForm: {
        name: '',
        email: '',
        password: '',
        accountType: 'personal'
      }
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = '';
      this.successMessage = '';

      try {
        const data = await api.login({
          email: this.loginForm.email,
          password: this.loginForm.password
        });

        // Save JWT token
        sessionStorage.setItem('authToken', data.token);
        
        // Save user info if available
        if (data.user) {
          sessionStorage.setItem('user', JSON.stringify(data.user));
        }

        this.successMessage = 'Login successful! Redirecting...';
        
        // Redirect to dashboard
        setTimeout(() => {
          this.$router.push('/dashboard');
        }, 1500);
      } catch (error) {
        this.errorMessage = error.message || 'Login failed. Please try again.';
        console.error('Login error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async handleRegister() {
      this.isLoading = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const data = await api.register({
          name: this.registerForm.name,
          email: this.registerForm.email,
          password: this.registerForm.password,
          accountType: this.registerForm.accountType
        });

        // Save JWT token
        sessionStorage.setItem('authToken', data.token);
        
        // Save user info
        if (data.user) {
          sessionStorage.setItem('user', JSON.stringify(data.user));
        }

        this.successMessage = 'Account created successfully! Redirecting...';
        
        // Redirect to dashboard
        setTimeout(() => {
          this.$router.push('/dashboard');
        }, 1500);
      } catch (error) {
        this.errorMessage = error.message || 'Registration failed. Please try again.';
        console.error('Registration error:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.animation-delay-2s {
  animation-delay: 2s;
}

.animation-delay-4s {
  animation-delay: 4s;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.5);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 92, 246, 0.7);
}
</style>