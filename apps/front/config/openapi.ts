import { Configuration } from "components/generated/api";

export function Config() {
  return new Configuration({ basePath: process.env.NEXT_PUBLIC_API_PATH });
}
