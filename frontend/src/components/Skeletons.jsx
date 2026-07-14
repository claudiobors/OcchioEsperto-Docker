export function CardSkeleton() {
  return (
    <div className="bg-white rounded-2xl border border-vespa-cream-dark overflow-hidden animate-pulse">
      <div className="h-40 bg-vespa-cream-dark/50" />
      <div className="p-4 space-y-3">
        <div className="h-5 bg-vespa-cream-dark/50 rounded w-3/4" />
        <div className="h-3 bg-vespa-cream-dark/50 rounded w-1/2" />
        <div className="flex justify-between items-center pt-2">
          <div className="h-5 bg-vespa-cream-dark/50 rounded-full w-16" />
          <div className="h-4 bg-vespa-cream-dark/50 rounded w-4" />
        </div>
      </div>
    </div>
  )
}

export function GarageGridSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  )
}

export function StatsCardSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-vespa-cream-dark p-5 animate-pulse">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-vespa-cream-dark/50" />
        <div className="space-y-2 flex-1">
          <div className="h-3 bg-vespa-cream-dark/50 rounded w-1/3" />
          <div className="h-6 bg-vespa-cream-dark/50 rounded w-1/2" />
        </div>
      </div>
    </div>
  )
}

export function FormSkeleton() {
  return (
    <div className="bg-white rounded-2xl border border-vespa-cream-dark p-6 sm:p-8 animate-pulse space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-full bg-vespa-cream-dark/50" />
        <div className="space-y-2">
          <div className="h-5 bg-vespa-cream-dark/50 rounded w-40" />
          <div className="h-3 bg-vespa-cream-dark/50 rounded w-64" />
        </div>
      </div>
      <div className="h-32 bg-vespa-cream-dark/30 rounded-xl" />
      <div className="h-12 bg-vespa-cream-dark/30 rounded-xl" />
      <div className="h-12 bg-vespa-cream-dark/30 rounded-xl" />
      <div className="h-12 bg-vespa-cream-dark/30 rounded-xl" />
      <div className="h-12 bg-vespa-green/30 rounded-xl" />
    </div>
  )
}