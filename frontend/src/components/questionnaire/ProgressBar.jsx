export default function ProgressBar({ current, total }) {
  const percentage = (current / total) * 100;

  return (
    <div className="w-full max-w-3xl mx-auto mb-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-white font-medium">
          Progress
        </span>
        <span className="text-white font-semibold">
          {current}/{total}
        </span>
      </div>
      
      <div className="w-full h-4 bg-gray-900/50 rounded-full overflow-hidden border border-white/30">
        <div
          className="h-full bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 transition-all duration-500 ease-out shadow-lg"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      
      <div className="text-center mt-2">
        <span className="text-white/90 text-sm font-medium">
          {Math.round(percentage)}% Complete
        </span>
      </div>
    </div>
  );
}