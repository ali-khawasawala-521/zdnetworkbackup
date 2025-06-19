// plugins/fetch-interceptor.ts

import type { App } from 'vue'
import { toast } from 'vue-sonner'

const fetchInterceptor = {
  install(app: App) {
    const originalFetch = window.fetch

    window.fetch = async (input: RequestInfo, init?: RequestInit): Promise<Response> => {
      const method = init?.method?.toUpperCase() || 'GET'

      // Intercept only mutation methods
      if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        // Modify headers if needed
        //   init = {
        //     ...init,
        //     headers: {
        //       ...(init?.headers || {}),
        //       'X-Intercepted': 'true',
        //     }
        //   }
        // }

        try {
          const response = await originalFetch(input, init)
          const clonedResponse = response.clone()

          const data = await clonedResponse.json()
          if (!response.ok) {
            toast?.error(data.message || 'Something went wrong')
          } else {
            toast?.success(data.message)
          }

          return response
        } catch (error: any) {
          toast.error(`${error?.message || error || 'Something went wrong'}`)
          throw error
        }
      }

      return originalFetch(input, init)
    }
  },
}

export default fetchInterceptor
