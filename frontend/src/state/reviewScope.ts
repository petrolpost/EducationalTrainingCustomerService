export type ReviewScope = {
  principalId: string;
  roleTemplate: string;
  tenantId: string;
};

export function createDefaultReviewScope(): ReviewScope {
  return {
    principalId: "tenant-manager-a",
    roleTemplate: "tenant_manager",
    tenantId: "tenant-a"
  };
}
