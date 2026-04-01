type Props = {
  isActive: boolean;
};

export default function ScheduledTaskStatusBadge({ isActive }: Props) {
  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${
        isActive
          ? "bg-green-100 text-green-700"
          : "bg-zinc-200 text-zinc-700"
      }`}
    >
      {isActive ? "Activa" : "Inactiva"}
    </span>
  );
}