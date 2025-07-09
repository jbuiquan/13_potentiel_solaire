import { TabId } from "../components/fiches/Fiches";
import { Codes } from "./hooks/useURLParams";


export const ACTIVE_TAB_KEY = 'activeTab';

export function buildActiveTabParam(tabId: TabId): URLSearchParams {
	return new URLSearchParams({ [ACTIVE_TAB_KEY]: tabId });
}

export function buildCodesParam(codes: Record<keyof Codes, string>): URLSearchParams {
	return new URLSearchParams({ ...codes });
}
