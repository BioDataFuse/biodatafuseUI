<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo and main nav -->
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-semibold text-indigo-600">BioDataFuse</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                v-for="item in navigation" 
                :key="item.name"
                :to="item.to"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="[$route.path === item.to ? 'border-b-2 border-indigo-500 text-gray-900' : 'text-gray-500 hover:text-gray-700']"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>

          <!-- User menu -->
          <div class="flex items-center">
            <template v-if="isAuthenticated">
              <router-link 
                to="/profile" 
                class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              >
                Profile
              </router-link>
              <button 
                @click="logout"
                class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              >
                Sign out
              </button>
            </template>
            <template v-else>
              <router-link 
                to="/login" 
                class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              >
                Sign in
              </router-link>
              <router-link 
                to="/register" 
                class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Sign up
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-white">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 md:flex md:items-center md:justify-between lg:px-8">
        <div class="mt-8 md:mt-0 md:order-1">
          <p class="text-center text-base text-gray-400">
            &copy; 2026 BioDataFuse
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isAuthenticated = computed(() => auth.isAuthenticated)

const navigation = [
  { name: 'Home', to: '/' },
  { name: 'Query', to: '/query' },
  { name: 'Visualize and Analysis', to: '/visualize&analysis' },
  { name: 'Documentation', to: '/documentation' },
  { name: 'Contact', to: '/contact' },
  { name: 'About', to: '/about' }
]

async function logout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>