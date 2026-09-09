/**
 * API Client for Financial Crime Knowledge Engine
 * 
 * Provides a typed, centralized way to interact with the backend API.
 * This is the foundation that will be expanded in future phases.
 */

// Base configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// API Response wrapper type
export interface ApiResponse<T> {
  data: T | null;
  error: ApiError | null;
  status: number;
  success: boolean;
}

// Error response shape
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

// Health check response types (Phase 0)
export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  version: string;
  timestamp?: string;
}

export interface ReadinessResponse {
  status: "ready" | "not_ready";
  checks: {
    database: "ok" | "error";
    redis: "ok" | "error";
  };
}

export interface VersionResponse {
  version: string;
  phase: string;
  api_version: string;
}

/**
 * API Client class with typed methods
 */
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make an HTTP request to the API
   */
  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${path}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        return {
          data: null,
          error: {
            code: `HTTP_${response.status}`,
            message: data?.detail || data?.message || "Unknown error",
            details: data,
          },
          status: response.status,
          success: false,
        };
      }

      return {
        data,
        error: null,
        status: response.status,
        success: true,
      };
    } catch (error) {
      return {
        data: null,
        error: {
          code: "NETWORK_ERROR",
          message: error instanceof Error ? error.message : "Network request failed",
        },
        status: 0,
        success: false,
      };
    }
  }

  /**
   * Health check endpoint
   */
  async health(): Promise<ApiResponse<HealthResponse>> {
    return this.request<HealthResponse>("/health");
  }

  /**
   * Readiness probe endpoint
   */
  async ready(): Promise<ApiResponse<ReadinessResponse>> {
    return this.request<ReadinessResponse>("/ready");
  }

  /**
   * Version information endpoint
   */
  async version(): Promise<ApiResponse<VersionResponse>> {
    return this.request<VersionResponse>("/version");
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Also export class for custom instances
export default ApiClient;

// Type utilities for future expansion
export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export interface PaginationParams {
  page?: number;
  page_size?: number;
  offset?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}
