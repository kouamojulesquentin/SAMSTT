% -------------------------Data Collection----------------------------------
%-------------------------------------------------------------------
%------------------------------SISO--------------------------------
%------------------------------------------------------------------


%-------------------time-------------------------------------------
time_good = out.V_in_physical_good.Time;
time_faulty = out.V_in_physical_Fault_C_UP.Time;
time_TF_good = out.V_in_TF_good.Time;
time_TF_faulty = out.V_in_TF_Fault_C_UP.Time;

%-------------------V_in_----------------------------------------
V_in_good = out.V_in_physical_good.Data;
V_in_faulty = out.V_in_physical_Fault_C_UP.Data;
V_in_TF_good = out.V_in_TF_good.Data;
V_in_TF_faulty = out.V_in_TF_Fault_C_UP.Data;

%-------------------V_out_---------------------------------------
V_out_good = out.V_out_physical_good.Data;
V_out_faulty = out.V_out_physical_good.Data;
V_out_TF_good = out.V_out_TF_good.Data;
V_out_TF_faulty = out.V_out_TF_Fault_C_UP.Data;

% Convert to iddata
idata = iddata(V_out_good, V_in_good); 
idata_TF = iddata(V_out_TF_good, V_in_TF_good);
idata_Fault = iddata(V_out_faulty, V_in_faulty);

% Export data to CSV
data_2_good = [time_good, V_in_good, V_out_good];
data_2_faulty = [time_faulty, V_in_faulty, V_out_faulty];
 
data_2_TF_good = [time_TF_good, V_in_TF_good, V_out_TF_good];
data_2_TF_faulty = [time_TF_faulty, V_in_TF_faulty, V_out_TF_faulty];

data_good_circuit = array2table(data_2_good, 'VariableNames', {'time','V_in','V_out'}); 
data_faulty_circuit = array2table(data_2_faulty, 'VariableNames', {'time','V_in','V_out'});
data_TF_good = array2table(data_2_TF_good, 'VariableNames', {'time','V_in','V_out'});
data_TF_faulty = array2table(data_2_TF_faulty, 'VariableNames', {'time','V_in','V_out'});


writetable(data_good_circuit, 'data_good_circuit.csv');
writetable(data_faulty_circuit, 'data_faulty_circuit.csv');
writetable(data_TF_good, 'data_TF_good.csv');
writetable(data_TF_faulty, 'data_TF_faulty.csv');





