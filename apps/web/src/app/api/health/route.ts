import { NextResponse } from "next/server";

/**
 * Health check endpoint for the web application.
 * 
 * In production, this would proxy to the backend API health endpoint.
 * For Phase 0, it returns a simple status to verify the frontend is running.
 */
export async function GET() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  
  try {
    // Attempt to fetch from backend API
    const response = await fetch(`${apiUrl}/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      // Don't wait too long for backend
      signal: AbortSignal.timeout(5000),
    });

    if (response.ok) {
      const data = await response.json();
      return NextResponse.json({
        status: "healthy",
        service: "web",
        version: process.env.APP_VERSION || "0.1.0",
        backend: data,
      });
    }

    // Backend not healthy but frontend is
    return NextResponse.json({
      status: "degraded",
      service: "web",
      version: process.env.APP_VERSION || "0.1.0",
      backend: {
        status: "unavailable",
        message: `Backend returned status ${response.status}`,
      },
    });
  } catch (error) {
    // Backend unreachable but frontend is working
    return NextResponse.json({
      status: "degraded",
      service: "web",
      version: process.env.APP_VERSION || "0.1.0",
      backend: {
        status: "unreachable",
        message: error instanceof Error ? error.message : "Unknown error",
      },
    });
  }
}
