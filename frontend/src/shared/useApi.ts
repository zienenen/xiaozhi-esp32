import { useCallback, useEffect, useState } from "react";
import { readableError } from "./api";

export function useApiData<T>(loader: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const load = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    setError(null);
    try { setData(await loader()); } catch (reason) { setError(readableError(reason)); } finally { setLoading(false); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  useEffect(() => { void load(); }, [load]);
  const reload = useCallback(() => load(), [load]);
  const silentReload = useCallback(() => load(true), [load]);
  return { data, loading, error, reload, silentReload, setData };
}
