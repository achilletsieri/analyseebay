interface Project {
  title: string;
  sector: string;
  city: string;
  imageUrl: string | null;
}

export function ProjectMockup({ project }: { project: Project }) {
  const fakeUrl = `www.${project.sector}-${project.city.toLowerCase().replace(/\s/g, "")}.fr`;

  return (
    <div className="mb-8 overflow-hidden rounded-xl border bg-white shadow-lg">
      <div className="flex items-center gap-2 border-b bg-gray-100 px-4 py-3">
        <div className="h-3 w-3 rounded-full bg-red-400" />
        <div className="h-3 w-3 rounded-full bg-yellow-400" />
        <div className="h-3 w-3 rounded-full bg-green-400" />
        <div className="ml-4 flex-1 rounded-md bg-white px-3 py-1 text-sm text-gray-500">
          https://{fakeUrl}
        </div>
      </div>
      <div className="relative h-64 bg-gradient-to-br from-blue-50 to-indigo-100 md:h-96">
        {project.imageUrl ? (
          <img src={project.imageUrl} alt={project.title} className="h-full w-full object-cover" />
        ) : (
          <div className="flex h-full flex-col items-center justify-center gap-4 text-blue-300">
            <span className="text-6xl">🌐</span>
            <p className="text-lg font-medium">Mockup à générer</p>
          </div>
        )}
      </div>
    </div>
  );
}
