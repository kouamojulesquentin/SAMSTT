function values_to_return = identify_armax_model(csv_file, na, nb)

    data = readtable(csv_file);
    

    if ~all(ismember({'time', 'V_in', 'V_out'}, data.Properties.VariableNames))
        error('CSV file must contain columns: time, V_in, V_out');
    end


    time = data.time;
    V_in = data.V_in;
    V_out = data.V_out;

    data_id = iddata(V_out, V_in, mean(diff(time)));

    nc = 2; % Order of the noise input part
    nk = 1; % Input delay


    model = armax(data_id, [na nb nc nk]);
     transfer_function = tf(model);


    Numerators = transfer_function.Numerator{1, 1};
    Denominators = transfer_function.Denominator{1, 1};
    values_to_return = [Numerators, Denominators];
    

end
