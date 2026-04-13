# Server-Side Search, Filtering, Pagination & Easier Modification

## Summary
Add Django pagination + role filter to ContactViewSet; add inline edit for contacts and projects in the React frontend.

### [x] Step: Django backend — pagination + role filter
- Added `ContactPagination` (PageNumberPagination) returning `count`, `total_pages`, `current_page`, `results`
- Added `ContactFilter` (FilterSet) with `role` icontains and `company` id filter
- Applied `pagination_class = ContactPagination` and `filterset_class = ContactFilter` to `ContactViewSet`
- File: `contacts/views.py`

### [x] Step: React frontend — inline edit for contacts
- Added `editingId` / `editForm` state
- Edit button (✎) on each contact card opens an inline form pre-filled with existing data
- Save calls `updateContact` (PATCH) then re-fetches the current filtered page
- File: `src/pages/Contacts.jsx` in personal-erp-frontend

### [x] Step: React frontend — inline edit for projects
- Added `editingProjectId` / `editProjectForm` state
- Edit button (✎) on each project card opens an inline edit form for name, description, status, due_date
- Save calls `updateProject` (PATCH) and updates local state
- File: `src/pages/Projects.jsx` in personal-erp-frontend
