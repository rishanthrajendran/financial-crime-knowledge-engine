import { Shield, Server, Database, Cpu, CheckCircle2, Clock, Circle } from "lucide-react";
import Link from "next/link";

// System status configuration - HONEST status for Phase 0
const SYSTEM_STATUS = {
  name: "Financial Crime Knowledge Engine",
  phase: "Phase 0 - Software Foundation",
  version: "0.1.0",
  knowledgeBaseVersion: "v3.0.1 LTS",
} as const;

interface ComponentStatus {
  name: string;
  status: "implemented" | "scaffolded" | "planned" | "specification_only";
  description: string;
}

const COMPONENT_STATUSES: ComponentStatus[] = [
  // Implemented components
  {
    name: "Monorepo Structure",
    status: "implemented",
    description: "pnpm workspaces with apps/* and packages/*",
  },
  {
    name: "Next.js Frontend Shell",
    status: "implemented",
    description: "Landing page with system status display",
  },
  {
    name: "FastAPI Backend Foundation",
    status: "implemented",
    description: "Health checks, config, database setup",
  },
  {
    name: "Docker Configuration",
    status: "implemented",
    description: "docker-compose with all services",
  },
  {
    name: "CI/CD Pipeline",
    status: "implemented",
    description: "GitHub Actions with lint, test, build jobs",
  },

  // Scaffolded components
  {
    name: "Worker Framework",
    status: "scaffolded",
    description: "Job execution model and registry (structure only)",
  },
  {
    name: "Database Schema",
    status: "scaffolded",
    description: "Alembic migrations defined (not yet applied)",
  },

  // Planned components
  {
    name: "Authentication & RBAC",
    status: "planned",
    description: "User management and role-based access (Phase 1)",
  },
  {
    name: "Knowledge Ingestion Pipeline",
    status: "planned",
    description: "Import from Knowledge Base repository (Phase 1)",
  },
  {
    name: "Vector Search / RAG",
    status: "planned",
    description: "AI-powered semantic search (Phase 2)",
  },
  {
    name: "Graph Search",
    status: "planned",
    description: "Relationship-based knowledge queries (Phase 2)",
  },
  {
    name: "Assessment Engine",
    status: "planned",
    description: "Automated risk assessment workflows (Phase 3)",
  },
];

function StatusIcon({ status }: { status: ComponentStatus["status"] }) {
  switch (status) {
    case "implemented":
      return <CheckCircle2 className="h-5 w-5 text-emerald-600" />;
    case "scaffolded":
      return <Clock className="h-5 w-5 text-amber-600" />;
    case "planned":
      return <Circle className="h-5 w-5 text-gray-400" />;
    case "specification_only":
      return <Circle className="h-5 w-5 text-blue-400" />;
  }
}

function StatusBadge({ status }: { status: ComponentStatus["status"] }) {
  const styles = {
    implemented:
      "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200",
    scaffolded:
      "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
    planned:
      "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200",
    specification_only:
      "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  };

  const labels = {
    implemented: "IMPLEMENTED",
    scaffolded: "SCAFFOLDED",
    planned: "PLANNED",
    specification_only: "SPEC ONLY",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}

export default function HomePage() {
  const implementedCount = COMPONENT_STATUSES.filter(
    (c) => c.status === "implemented"
  ).length;
  const totalCount = COMPONENT_STATUSES.length;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary">
              <Shield className="h-7 w-7 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                {SYSTEM_STATUS.name}
              </h1>
              <p className="text-sm text-muted-foreground">
                {SYSTEM_STATUS.phase}
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Version Info Cards */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-10">
          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Server className="h-8 w-8 text-primary" />
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Software Version
                </p>
                <p className="text-2xl font-bold text-foreground">
                  {SYSTEM_STATUS.version}
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Database className="h-8 w-8 text-primary" />
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Knowledge Base
                </p>
                <p className="text-2xl font-bold text-foreground">
                  {SYSTEM_STATUS.knowledgeBaseVersion}
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Cpu className="h-8 w-8 text-primary" />
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Components Ready
                </p>
                <p className="text-2xl font-bold text-foreground">
                  {implementedCount}/{totalCount}
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8 text-primary" />
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Status
                </p>
                <p className="text-2xl font-bold text-emerald-600">
                  ACTIVE
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="mb-10 rounded-lg border border-border bg-card p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-foreground mb-4">
            Quick Links
          </h2>
          <div className="flex flex-wrap gap-4">
            <Link
              href="/api/health"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Health Check →
            </Link>
            <Link
              href="/docs"
              className="inline-flex items-center rounded-md border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent transition-colors"
            >
              API Docs (Coming Soon)
            </Link>
            <a
              href="https://github.com/fcke/financial-crime-knowledge-engine"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center rounded-md border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-accent transition-colors"
            >
              GitHub Repository
            </a>
          </div>
        </div>

        {/* Component Status Table */}
        <div className="rounded-lg border border-border bg-card shadow-sm">
          <div className="px-6 py-4 border-b border-border">
            <h2 className="text-lg font-semibold text-foreground">
              Implementation Status
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              Honest assessment of current implementation state
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border bg-muted/50">
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    Component
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground hidden sm:table-cell">
                    Description
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {COMPONENT_STATUSES.map((component) => (
                  <tr key={component.name} className="hover:bg-muted/30 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-3">
                        <StatusIcon status={component.status} />
                        <span className="text-sm font-medium text-foreground">
                          {component.name}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <StatusBadge status={component.status} />
                    </td>
                    <td className="px-6 py-4 text-sm text-muted-foreground hidden sm:table-cell">
                      {component.description}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 flex flex-wrap gap-6 justify-center text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
            <span>Implemented - Working code</span>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-amber-600" />
            <span>Scaffolded - Structure exists</span>
          </div>
          <div className="flex items-center gap-2">
            <Circle className="h-4 w-4 text-gray-400" />
            <span>Planned - Design complete</span>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-muted-foreground">
              © 2024 Financial Crime Knowledge Engine. MIT License.
            </p>
            <p className="text-xs text-muted-foreground">
              Phase 0 - Software Foundation • Version {SYSTEM_STATUS.version}
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
